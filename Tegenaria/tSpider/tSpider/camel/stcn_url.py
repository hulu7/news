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
import time
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class Stcn():
    def getSettings(self):
        self.work_path_prd2 = Settings.STCN['WORK_PATH_PRD2']
        self.finished_url_path = Settings.STCN['FINISHED_URL_PATH']
        self.mongo = Settings.STCN['MONGO_URLS']
        self.name = Settings.STCN['NAME']
        self.max_pool_size = Settings.STCN['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.STCN['URLS']
        self.restart_path = Settings.STCN['RESTART_PATH']
        self.restart_interval = Settings.STCN['RESTART_INTERVAL']

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

    def isExceedRestartInterval(self):
        isRestartPathExists = os.path.exists(self.restart_path)
        if isRestartPathExists is False:
            self.file.writeToTxtCover(self.restart_path, time.time())
            return True
        past = float(self.file.readFromTxt(self.restart_path))
        now = time.time()
        isExceed = (now - past) // 60 >= self.restart_interval
        if isExceed is True:
            self.file.writeToTxtCover(self.restart_path, time.time())
        return isExceed

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")
        keys = ['certificate', 'pdf', 'video', 'filepublish']
        for item in href_items:
            href = item.xpath("@href")
            hasKeys = False
            if len(href) == 0:
                continue
            if len(str(filter(str.isdigit, href[0]))) == 0:
                continue
            if 'html' not in href[0]:
                continue
            for key in keys:
                if key in href[0]:
                    hasKeys = True
            if hasKeys == True:
                continue
            short_url = href[0]
            short_url_parts = re.split(r'[., /, _]', short_url)
            id = short_url_parts[len(short_url_parts) - 2]
            url = urlparse.urljoin(current_url, short_url)
            title = item.xpath("@title")
            if len(title) == 0:
                continue
            title = title[0]
            is_finished = self.idInStoredFormat(id) in self.finished_ids

            if is_finished is False:
                data = {
                    'title': title.strip(),
                    'url': url.strip(),
                    'id': id.strip()
                }
                self.storeMongodb(data)
                self.file.logger(self.log_path, 'End to parse: {0}'.format(current_url))
            else:
                print 'Empty title for: {0}'.format(url)

        print 'End to parse: {0}'.format(current_url)

    def start_requests(self):
        self.init()
        if self.isExceedRestartInterval() is False:
            return
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        self.finished_ids = self.readFinishedIds().tolist()
        new_urls = self.urls
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End requests: {0}'.format(str(len(content))))
        print 'End requests: {0}'.format(str(len(content)))

if __name__ == '__main__':
    stcn=Stcn()
    stcn.start_requests()