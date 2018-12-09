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
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class Huxiu():
    def getSettings(self):
        self.work_path_prd2 = Settings.HUXIU['WORK_PATH_PRD2']
        self.finished_url_path = Settings.HUXIU['FINISHED_URL_PATH']
        self.mongo = Settings.HUXIU['MONGO_URLS']
        self.name = Settings.HUXIU['NAME']
        self.max_pool_size = Settings.HUXIU['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2

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
            print 'Start to store mongo %s' % item['url']
            mongo.insert( self.mongo, item)
            self.storeFinishedIds(str(item['id']))
            self.file.logger(self.log_path, 'End to store mongo %s' % item['url'])
            print 'End to store mongo %s' % item['url']

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse %s' % current_url
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//*[contains(@class,'transition msubstr-row2')]")
        data = []
        for item in href_items:
            short_url = item.xpath("@href")[0]
            id = str(filter(str.isdigit, short_url.encode('gbk')))
            url = urlparse.urljoin(current_url, short_url)
            finished_ids = self.readFinishedIds()
            if [int(id)] not in finished_ids:
                title = item.text
                data.append({
                    'title': title,
                    'url': url,
                    'id': id
                })
            else:
                print 'Url exits %s' % url
        self.storeMongodb(data)
        self.file.logger(self.log_path, 'End to parse %s' % current_url)
        print 'End to parse %s' % current_url

    def start_requests(self, urls):
        self.init()
        self.file.logger(self.log_path, 'Start '+ self.name +' requests')
        print 'Start ' + self.name + ' requests'
        new_urls = urls
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, callback=self.parse)
        self.file.logger(self.log_path, 'End %s requests' % str(len(content)))
        print 'End %s requests' % str(len(content))

if __name__ == '__main__':
    huxiu=Huxiu()
    urls = ['https://www.huxiu.com/']
    huxiu.start_requests(urls)