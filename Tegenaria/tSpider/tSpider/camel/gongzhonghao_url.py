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

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'gzh-box')]//a/@href")
        if len(href_item) == 0:
            print 'Blocked for {0}'.format(key)
            return
        self.doraemon.hashSet(self.name, key, href_item[0])
        print 'Finished for {0}'.format(key)

        print 'End to parse {0}, url: {1}'.format(key, href_item[0])

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        new_urls = []
        for key in self.urls:
            timestamp = '00'.join(str(time.time()).split('.'))
            tmp_url = "https://weixin.sogou.com/weixinwap?ie=utf8&s_from=input&type=1&t={0}&pg=webSearchList&_sug_=n&_sug_type_=&query={1}".format(timestamp, key)
            new_urls.append([tmp_url, key])
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

if __name__ == '__main__':
    gongzhonghao=GongZhongHao()
    gongzhonghao.start_requests()