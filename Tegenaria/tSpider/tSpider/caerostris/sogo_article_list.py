# coding:utf-8
# ------requirement------
# lxml-3.2.1
# numpy-1.15.2
# ------requirement------
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import urlparse
import re
import requests
import time

sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon


class SogoArticleList():
    def __init__(self):
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('sogo')
        self.work_path_prd2 = settings_name['WORK_PATH_PRD2']
        self.mongo = settings_name['MONGO_URLS']
        self.name = settings_name['NAME']
        self.max_pool_size = settings_name['MAX_POOL_SIZE']
        self.log_path = self.settings.LOG_PATH_PRD2
        self.urls = settings_name['URLS']
        self.restart_path = settings_name['RESTART_PATH']
        self.restart_interval = settings_name['RESTART_INTERVAL']
        self.valid_proxy_pool_sogo_article_list = self.settings.VALID_PROXY_POOL_SOGO_ARTICLE_LIST
        self.invalid_proxy_pool_sogo_article_list = self.settings.INVALID_PROXY_POOL_SOGO_ARTICLE_LIST
        self.finished_sogo_article_list = self.settings.FINISHED_SOGO_ARTICLE_LIST

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'gzh-box')]//a/@href")
        if len(href_item) == 0:
            self.doraemon.hashSet(self.invalid_proxy_name, self.proxy, self.proxy)
            self.doraemon.delHashSet(self.valid_proxy_name, self.proxy)
        self.doraemon.hashSet(self.name, key, href_item[0])
        self.doraemon.hashSet(self.finished_gongzhonghao_id, key, key)
        self.current_url.pop()
        print 'Finished for {0}'.format(key)
        if len(self.new_urls) > 0:
            new_url = self.new_urls.pop()
            print 'Start next: {0}'.format(new_url[0])
            self.current_url.append(new_url)
        print 'End to parse {0}, url: {1}'.format(key, href_item[0])

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.new_urls = []
        self.current_url = []

        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_gongzhonghao_id))
        all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_name))

        self.proxy = all_valid_proxy.pop()
        for key in self.urls:
            if key not in all_finished_id:
                timestamp = '00'.join(str(time.time()).split('.'))
                tmp_url = "https://weixin.sogou.com/weixinwap?ie=utf8&s_from=input&type=1&t={0}&pg=webSearchList&_sug_=n&_sug_type_=&query={1}".format(
                    timestamp, key)
                self.new_urls.append([tmp_url, key])

        request = BrowserRequest()
        if len(self.new_urls) > 0:
            self.current_url.append(self.new_urls.pop())
        else:
            print 'No more urls.'
        while len(self.current_url) > 0:
            request.start_chrome(self.current_url, self.max_pool_size, self.log_path, self.proxy, callback=self.parse)

        self.file.logger(self.log_path, 'End for requests of {0}.'.format(self.name))

if __name__ == '__main__':
    SogoArticleList = SogoArticleList()
    SogoArticleList.start_requests()