#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import urlparse
import numpy as np
import re
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class Sp():
    def getSettings(self):
        self.work_path_prd2 = Settings.SP['WORK_PATH_PRD2']
        self.finished_url_path = Settings.SP['FINISHED_URL_PATH']
        self.mongo = Settings.SP['MONGO_URLS']
        self.name = Settings.SP['NAME']
        self.max_pool_size = Settings.SP['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.SP['URLS']

    def init(self):
        self.getSettings()
        self.file = FileIOMiddleware()
        isWorkPathPrd2Exists = os.path.exists(self.work_path_prd2)
        if isWorkPathPrd2Exists is False:
            os.makedirs(self.work_path_prd2)
        isFinishedUrlPathExists = os.path.exists(self.finished_url_path)
        if isFinishedUrlPathExists is False:
            self.file.writeToCSVWithoutHeader(self.finished_url_path, ['id'])
        isLogPathExists = os.path.exists(Settings.LOG_PATH)
        if isLogPathExists is False:
            os.makedirs(Settings.LOG_PATH)

    def readFinishedIds(self):
        print 'Start to read finihsed urls'
        isFinishedIdsPathExit = os.path.exists(self.finished_url_path)
        finished_ids = []
        if isFinishedIdsPathExit is True:
            finished_ids = np.array(self.file.readColsFromCSV(self.finished_url_path, ['id']))
        return finished_ids

    def storeFinishedIds(self, id):
        print 'Start to store finished id %s' % id
        self.file.writeToCSVWithoutHeader(self.finished_url_path, [id.replace('\xef\xbb\xbf','')])
        print 'End to store finished id %s' % id

    def storeMongodb(self, data):
        mongo = MongoMiddleware()
        for item in data:
            finished_ids = self.readFinishedIds()
            if [int(item['id'])] in finished_ids:
                self.file.logger(self.log_path, 'Url exits %s' % item['url'])
                continue
            self.file.logger(self.log_path, 'Start to store mongo %s' % item['url'])
            print 'Start to store mongo: %s' % item['url']
            mongo.insert( self.mongo, item)
            self.storeFinishedIds(str(item['id']))
            self.file.logger(self.log_path, 'End to store mongo %s' % item['url'])
            print 'End to store mongo: %s' % item['url']

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse %s' % current_url
        html = etree.HTML(response['response'].page_source)
        items_list = html.xpath(".//li[contains(@class,'accbg')]")
        data = []
        for item in items_list:
            short_url = item.xpath(".//*[contains(@class,'leaidx')]/@href")[0]
            id = re.split(r'[., /, _]', short_url)[4]
            url = urlparse.urljoin(current_url, short_url)
            finished_ids = self.readFinishedIds()
            if [int(id)] not in finished_ids:
                title = item.xpath(".//*[contains(@class,'leaidx')]/text()")[0]
                time = re.split(r'[\[, \]]', item.xpath(".//*[contains(@class,'date leaidx')]/text()")[0])[1]
                data.append({
                    'title': title,
                    'url': url,
                    'time': time,
                    'id': id
                })
            else:
                print 'Url exits %s' % url
        self.storeMongodb(data)
        self.file.logger(self.log_path, 'End to parse %s' % current_url)
        print 'End to parse %s' % current_url

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start '+ self.name +' requests')
        print 'Start ' + self.name + ' requests'
        new_urls = self.urls
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, callback=self.parse)
        self.file.logger(self.log_path, 'End %s requests' % str(len(content)))
        print 'End %s requests' % str(len(content))

if __name__ == '__main__':
    sp=Sp()
    sp.start_requests()