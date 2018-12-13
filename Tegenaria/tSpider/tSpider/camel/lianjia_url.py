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

class Lianjia():
    def getSettings(self):
        self.work_path_prd2 = Settings.LIANJIA['WORK_PATH_PRD2']
        self.finished_url_path = Settings.LIANJIA['FINISHED_URL_PATH']
        self.mongo = Settings.LIANJIA['MONGO_URLS']
        self.name = Settings.LIANJIA['NAME']
        self.max_pool_size = Settings.LIANJIA['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.LIANJIA['URLS']

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
        print 'Start to store finished id {0}'.format(id)
        self.file.writeToCSVWithoutHeader(self.finished_url_path, [id.replace('\xef\xbb\xbf','')])
        print 'End to store finished id {0}'.format(id)

    def storeMongodb(self, data):
        mongo = MongoMiddleware()
        finished_ids = self.readFinishedIds()
        if [int(data['id'])] in finished_ids:
            self.file.logger(self.log_path, 'Url exits {0}'.format(data['url']))
            return
        self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
        print 'Start to store mongo {0}'.format(data['url'])
        mongo.insert(self.mongo, data)
        self.storeFinishedIds(str(data['id']))
        self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
        print 'End to store mongo {0}'.format(data['url'])

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        badkeys = ['']
        goodkeys = ['']
        print 'Start to parse %s' % current_url
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//*[contains(@class,'info clear')]")
        if len(href_items) == 0:
            return
        for item in href_items:
            href_list = item.xpath(".//*[contains(@class,'title')]/a/@href")
            valid = True
            href_url = href_list[0]
            if valid:
                id = item.xpath(".//*[contains(@class,'title')]/a/@data-housecode")
                url = urlparse.urljoin(current_url, href_url)
                title_list = item.xpath(".//*[contains(@class,'title')]/a/text()")
                price_list = item.xpath(".//*[contains(@class,'totalPrice')]/span/text()")
                finished_ids = self.readFinishedIds()
                if ([int(id[0])] not in finished_ids) and (len(title_list) > 0) and (len(price_list) > 0):
                    data = {
                        'title': title_list[0].strip(),
                        'url': url.strip(),
                        'id': id[0].strip(),
                        'price': price_list[0].strip()
                    }
                    self.storeMongodb(data)
                    self.file.logger(self.log_path, 'Done for {0}'.format(url))
                else:
                    self.file.logger(self.log_path, 'Invalid {0}'.format(url))
                    print 'Invalid {0}'.format(url)
            else:
                self.file.logger(self.log_path, 'Invalid {0}'.format(href_url))
                print 'Invalid {0}'.format(href_url)
        print 'End to parse {0}'.format(href_url)

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        new_urls = self.urls
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, callback=self.parse)
        self.file.logger(self.log_path, 'End %s requests' % str(len(content)))
        print 'End %s requests' % str(len(content))

if __name__ == '__main__':
    lianjia=Lianjia()
    lianjia.start_requests()