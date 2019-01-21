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

class Eeo():
    def getSettings(self):
        self.work_path_prd2 = Settings.EEO['WORK_PATH_PRD2']
        self.finished_url_path = Settings.EEO['FINISHED_URL_PATH']
        self.mongo = Settings.EEO['MONGO_URLS']
        self.name = Settings.EEO['NAME']
        self.max_pool_size = Settings.EEO['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.EEO['URLS']
        self.restart_path = Settings.EEO['RESTART_PATH']
        self.restart_interval = Settings.EEO['RESTART_INTERVAL']

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

    def idInStoredFormat(self, id):
        return [int(id)]

    def isEmpty(self, item_list):
        return len([item for item in item_list if item.strip()]) == 0

    def storeMongodb(self, data):
        mongo = MongoMiddleware()
        self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
        print 'Start to store mongo {0}'.format(data['url'])
        mongo.insert(self.mongo, data)
        self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
        print 'End to store mongo {0}'.format(data['url'])
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
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            hasId = str(filter(str.isdigit, href_url))
            if len(hasId) == 0:
                print 'Invalid url for no id: {0}'.format(href_url)
                continue
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
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                title = ""
                title_list1 = item.xpath(".//h5")
                title_list2 = item.xpath(".//text()")
                if len(title_list1) > 0:
                    title = title_list1[0].text
                    print title
                if len(title_list2) > 0:
                    title = title_list2[0]
                    print title
                is_finished = self.idInStoredFormat(id) in self.finished_ids
                is_title_empty = self.isEmpty(title)
                if (is_finished is False) and (is_title_empty is False):
                    data = {
                        'title': title.strip(),
                        'url': url.strip(),
                        'id': id.strip()
                    }
                    self.storeMongodb(data)
                    self.file.logger(self.log_path, 'Done for {0}'.format(url))
                else:
                    if is_title_empty is True:
                        self.file.logger(self.log_path, 'Empty title for {0}'.format(url))
                        print 'Empty title for {0}'.format(url)
                    print 'Finished or Empty title for {0}'.format(url)
            else:
                self.file.logger(self.log_path, 'Invalid {0}'.format(href_url))
                print 'Invalid {0}'.format(href_url)
        print 'End to parse {0}'.format(href_url)

    def start_requests(self):
        self.init()
        if self.isExceedRestartInterval() is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.badkeys = []
        self.goodkeys = []
        self.finished_ids = self.readFinishedIds().tolist()
        new_urls = self.urls
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests'.format(str(len(content))))
        print 'End for {0} requests'.format(str(len(content)))

if __name__ == '__main__':
    eeo=Eeo()
    eeo.start_requests()