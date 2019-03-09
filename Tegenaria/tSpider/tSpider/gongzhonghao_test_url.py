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

class Chuansongme():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.CHUANSONGME['WORK_PATH_PRD2']
        self.mongo = Settings.CHUANSONGME['MONGO_URLS']
        self.name = Settings.CHUANSONGME['NAME']
        self.max_pool_size = Settings.CHUANSONGME['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.CHUANSONGME['URLS']
        self.restart_path = Settings.CHUANSONGME['RESTART_PATH']
        self.restart_interval = Settings.CHUANSONGME['RESTART_INTERVAL']
        self.finished_ids = Settings.CHUANSONGME['FINISHED_IDS']

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'user')]/@href")
        if len(href_item) == 0:
            print 'No data for: {0}'.format(key)
            return
        href_url = href_item[0]
        url = urlparse.urljoin(current_url, href_url)
        self.doraemon.hashSet(self.finished_ids, key, key)
        data = {
            'id': key,
            'url': url.strip()
        }
        print 'Start to store mongo {0}'.format(data['url'])
        self.doraemon.storeMongodb(self.mongo, data)
        self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
        print 'Finished for {0}'.format(key)
        print 'End to parse {0}, url: {1}'.format(key, href_item[0])

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        new_urls = []
        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_ids))

        for key in self.urls:
            if key not in all_finished_id:
                tmp_url = "https://chuansongme.com/search?q={0}".format(key)
                self.new_urls.append([tmp_url, key])

        if len(self.new_urls) == 0:
            print 'No more urls.'
            return

        chuansongme = self.file.readFromTxt('/home/dev/Repository/news/Tegenaria/tSpider/tSpider/food/chuansongme.txt')
        all = chuansongme.split('\n')
        test = 0

        request = BrowserRequest()
        request.start_chrome(self.new_urls, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End for requests of {0}.'.format(self.name))

if __name__ == '__main__':
    Chuansongme=Chuansongme()
    Chuansongme.start_requests()