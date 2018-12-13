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

class Ifeng():
    def getSettings(self):
        self.work_path_prd2 = Settings.IFENG['WORK_PATH_PRD2']
        self.finished_url_path = Settings.IFENG['FINISHED_URL_PATH']
        self.mongo = Settings.IFENG['MONGO_URLS']
        self.name = Settings.IFENG['NAME']
        self.max_pool_size = Settings.IFENG['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.IFENG['URLS']

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
        finished_ids = self.readFinishedIds()
        if [data['id']] in finished_ids:
            self.file.logger(self.log_path, 'Url exits %s' % data['url'])
            return
        self.file.logger(self.log_path, 'Start to store mongo %s' % data['url'])
        print 'Start to store mongo %s' % data['url']
        mongo.insert(self.mongo, data)
        self.storeFinishedIds(str(data['id']))
        self.file.logger(self.log_path, 'End to store mongo %s' % data['url'])
        print 'End to store mongo %s' % data['url']

    def isEmpty(self, item_list):
        return len([item for item in item_list if item.strip()]) == 0

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse %s' % current_url
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")
        goodkeys = ['/a/', '/c/', 'detail']
        badkeys = ['jpg', 'yc', '#p', 'cosmetics', 'weidian', 'homedetail', 'detail?']

        for item in href_items:
            href = item.xpath("@href")
            valid = False
            if len(href) == 0:
                continue
            if item.xpath('.//text()') == None or self.isEmpty(item.xpath('.//text()')):
                continue
            for good in goodkeys:
                if valid == True:
                    continue
                if good in href[0]:
                    valid = True
            for bad in badkeys:
                if valid == False:
                    continue
                if bad in href[0]:
                    valid = False
            if valid == True:
                short_url = href[0].strip()
                if 'http' in short_url:
                    url = short_url
                else:
                    if '//' in short_url:
                        url = 'https:{0}'.format(short_url)
                    else:
                        url = urlparse.urljoin(current_url, short_url.strip())

                short_url_parts = re.split(r'[., /, _]', url)
                if '/a/' in short_url:
                    id_index = short_url_parts.index('a') + 2
                    id = short_url_parts[id_index].strip()
                if '/c/' in short_url:
                    id_index = short_url_parts.index('c') + 1
                    id = short_url_parts[id_index].strip()
                if 'detail' in short_url:
                    id_index = short_url_parts.index('detail') + 4
                    id = short_url_parts[id_index].strip()

                title = item.xpath(".//text()")
                if len(title) == 0:
                    continue
                title = title[0]
                finished_ids = self.readFinishedIds()
                if [id] not in finished_ids:
                    data = {
                        'title': title.strip(),
                        'url': url.strip(),
                        'id': id.strip()
                    }
                    self.storeMongodb(data)
                    self.file.logger(self.log_path, 'End to parse %s' % current_url)
                else:
                    print 'Url invalid %s' % url
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
    ifeng=Ifeng()
    ifeng.start_requests()