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

class Yicai():
    def getSettings(self):
        self.work_path_prd2 = Settings.YICAI['WORK_PATH_PRD2']
        self.finished_url_path = Settings.YICAI['FINISHED_URL_PATH']
        self.mongo = Settings.YICAI['MONGO_URLS']
        self.name = Settings.YICAI['NAME']
        self.max_pool_size = Settings.YICAI['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.YICAI['URLS']

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
        print 'Start to store finished id: {0}'.format(id)
        self.file.writeToCSVWithoutHeader(self.finished_url_path, [id.replace('\xef\xbb\xbf','')])
        print 'End to store finished id: {0}'.format(id)

    def idInStoredFormat(self, id):
        return [int(id)]

    def storeMongodb(self, data):
        mongo = MongoMiddleware()
        self.file.logger(self.log_path, 'Start to store mongo: {0}'.format(data['url']))
        print 'Start to store mongo: {0}'.format(data['url'])
        mongo.insert(self.mongo, data)
        self.file.logger(self.log_path, 'End to store mongo: {0}'.format(data['url']))
        print 'End to store mongo: {0}'.format(data['url'])
        self.storeFinishedIds(str(data['id']))
        self.finished_ids.append(self.idInStoredFormat(data['id']))

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")
        if len(href_items) == 0:
            return
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            if 'html' not in href_url:
                continue
            for good in self.goodkeys:
                if valid == True:
                    continue
                if good in href_url:
                    valid = True
            for bad in self.badkeys:
                if valid == False:
                    continue
                if bad in href_url:
                    valid = False
            if valid:
                title_content0_1 = item.xpath(".//div/h2/text()")
                title_content0_2 = item.xpath(".//div/h3/span/text()")
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                if len(title_content0_1) != 0:
                    title = title_content0_1[0]
                elif len(title_content0_2) != 0:
                    title = title_content0_2[0]
                else:
                    title = ""
                is_valid_id = len(str(filter(str.isdigit, id))) != 0
                is_finished = self.idInStoredFormat(id) in self.finished_ids
                is_title_empty = title == None
                if (is_valid_id is True) and (is_finished is False) and (is_title_empty is False):
                    data = {
                        'title': title,
                        'url': url,
                        'id': id
                    }
                    self.storeMongodb(data)
                    self.file.logger(self.log_path, 'End to parse: {0}'.format(current_url))
                else:
                    print 'Url exits or empty: {0}'.format(url)
                    if is_title_empty is True:
                        self.file.logger(self.log_path, 'Empty title for: {0}'.format(url))
                        self.storeFinishedIds(str(id))
                        print 'Empty title for {0}'.format(url)
        print 'End to parse: {0}'.format(current_url)

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        self.finished_ids = self.readFinishedIds().tolist()
        self.badkeys = ['daohang', 'video']
        self.goodkeys = ['']
        new_urls = self.urls
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End requests: {0}'.format(str(len(content))))
        print 'End requests: {0}'.format(str(len(content)))

if __name__ == '__main__':
    yicai=Yicai()
    yicai.start_requests()