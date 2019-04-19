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

class Weixin():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('wx')
        self.source = settings_name['SOURCE_NAME']
        self.work_path_prd2 = settings_name['WORK_PATH_PRD2']
        self.mongo = settings_name['MONGO_URLS']
        self.name = settings_name['NAME']
        self.max_pool_size = settings_name['MAX_POOL_SIZE']
        self.log_path = self.settings.LOG_PATH_PRD2
        self.urls = settings_name['URLS']
        self.restart_path = settings_name['RESTART_PATH']
        self.restart_interval = settings_name['RESTART_INTERVAL']

        self.valid_proxy_name = self.settings.VALID_PROXY_WX_URL

        self.invalid_proxy_name = self.settings.INVALID_PROXY_WX_URL
        self.finished_wx_id = self.settings.FINISHED_WX_ID

        self.finished_wx_aritcle_list_id = self.settings.FINISHED_WX_ARTICLE_LIST_ID

        self.today = self.settings.TODAY

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'weui_media_title')]/text()")
        if len(href_item) == 0:
            print "No content"
            return
        #     self.doraemon.hashSet(self.invalid_proxy_name, self.proxy, self.proxy)
        #     self.doraemon.delHashSet(self.valid_proxy_name, self.proxy)
        # self.doraemon.hashSet(self.finished_wx_aritcle_list_id, id, id)
        title = ''.join(href_item).strip()
        print title
        print self.count
        self.count += 1
        # self.current_url.pop()
        # print 'Finished for {0} -- id: {1}'.format(id, self.proxy)
        # self.file.logger(self.log_path, 'Finished for {0} -- id: {1}'.format(id, self.proxy))
        # if len(self.new_urls) > 0:
        #     new_url = self.new_urls.pop()
        #     print 'Start next: {0}'.format(new_url[0])
        #     self.current_url.append(new_url)
        # print 'End to parse {0}, url: {1}'.format(id, href_item[0])

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.new_urls = []
        self.current_url = []

        all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_name))
        # self.proxy = all_valid_proxy.pop()
        self.proxy = None
        finished_wx_aritcle_list_id = list(
            self.doraemon.getAllHasSet(self.finished_wx_aritcle_list_id))

        # self.urls_article_list = self.doraemon.getAllHasSet(self.url_pool)

        # for key in self.urls_article_list:
        #     url = self.urls_article_list[key]
        #     if key not in finished_wx_aritcle_list_id:
        #         self.new_urls.append([url, key])
        # if len(self.new_urls) > 0:
        #     self.current_url.append(self.new_urls.pop())
        # else:
        #     print 'No more urls.'
        #     return
        self.current_url = [['https://mp.weixin.qq.com/s?timestamp=1555455810&src=3&ver=1&signature=EHLmXR6NesCs9iuBl0SrFK6wHqPspj7zJIWDfOhXY1JPCjnAD8w469-xLwDFXIrJIiN7G4pLm2FcqrBFvCVobdHrvG9AwsUp5Nt-wvpgazEl2MvQPGi020W*K0Lz3gvQSHWzvnW5Li62GqmNGjGohTdyCy911T*ESQXm7O56CIk=', 'wx']]

        self.badkeys = ['None']
        self.goodkeys = ['']
        request = BrowserRequest()
        self.count = 0
        while len(self.current_url) > 0:
            request.start_chrome(self.current_url, self.max_pool_size, self.log_path, self.proxy, callback=self.parse)

        self.file.logger(self.log_path, 'End for requests of {0}.'.format(self.name))


if __name__ == '__main__':
    Weixin = Weixin()
    Weixin.start_requests()