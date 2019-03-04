#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
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

class GongZhongHao():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.GONGZHONGHAO['WORK_PATH_PRD2']
        self.mongo = Settings.GONGZHONGHAO['MONGO_URLS']
        self.name = Settings.GONGZHONGHAO['NAME']
        self.max_pool_size = Settings.GONGZHONGHAO['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.GONGZHONGHAO['URLS']
        self.restart_path = Settings.GONGZHONGHAO['RESTART_PATH']
        self.restart_interval = Settings.GONGZHONGHAO['RESTART_INTERVAL']
        self.proxy_pool = Settings.PROXY_POOL
        self.valid_proxy_name = Settings.VALID_PROXY_PARENT_URL
        self.finished_gongzhonghao_id = Settings.FINISHED_GONGZHONGHAO_ID
        self.invalid_proxy_name = Settings.INVALID_PROXY_PARENT_URL

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'gzh-box')]//a/@href")
        if len(href_item) == 0:
            self.doraemon.hashSet(self.invalid_proxy_name, self.proxy, self.proxy)
            self.doraemon.delHashSet(self.valid_proxy_name, self.proxy)
            all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_name))
            self.proxy = all_valid_proxy.pop()
            print 'Blocked for {0}'.format(key)
            return
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
        response = requests.get(self.proxy_pool)
        proxy_pool = eval(response.content)
        all_invalid_proxy = list(self.doraemon.getAllHasSet(self.invalid_proxy_name))
        for proxy in proxy_pool:
            ip_port = '{0}:{1}'.format(proxy[0], proxy[1])
            # valid_proxy.append(ip_port)
            if ip_port not in all_invalid_proxy:
                self.doraemon.hashSet(self.valid_proxy_name, ip_port, ip_port)
        all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_name))
        self.proxy = all_valid_proxy.pop()
        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_gongzhonghao_id))
        for key in self.urls:
            if key not in all_finished_id:
                timestamp = '00'.join(str(time.time()).split('.'))
                tmp_url = "https://weixin.sogou.com/weixinwap?ie=utf8&s_from=input&type=1&t={0}&pg=webSearchList&_sug_=n&_sug_type_=&query={1}".format(timestamp, key)
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
    gongzhonghao=GongZhongHao()
    gongzhonghao.start_requests()