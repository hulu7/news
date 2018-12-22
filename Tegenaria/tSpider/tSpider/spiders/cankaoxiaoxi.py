# -*- coding: utf-8 -*-
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import re
import numpy as np
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class Cankaoxiaoxi():
    def getSettings(self):
        self.work_path_prd1 = Settings.CANKAOXIAOXI['WORK_PATH_PRD1']
        self.finished_txt_path = Settings.CANKAOXIAOXI['FINISHED_TXT_PATH']
        self.finished_id_path = Settings.CANKAOXIAOXI['FINISHED_ID_PATH']
        self.url_path = Settings.CANKAOXIAOXI['URL_PATH']
        self.mongo = Settings.CANKAOXIAOXI['MONGO']
        self.name = Settings.CANKAOXIAOXI['NAME']
        self.max_pool_size = Settings.CANKAOXIAOXI['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH

    def init(self):
        self.getSettings()
        self.file = FileIOMiddleware()
        isWorkPathPrd1Exists = os.path.exists(self.work_path_prd1)
        if isWorkPathPrd1Exists is False:
            os.makedirs(self.work_path_prd1)
        isFinishedTxtPathExists = os.path.exists(self.finished_txt_path)
        if isFinishedTxtPathExists is False:
            os.makedirs(self.finished_txt_path)
        isLogPathExists = os.path.exists(Settings.LOG_PATH)
        if isLogPathExists is False:
            os.makedirs(Settings.LOG_PATH)
        del isWorkPathPrd1Exists, isFinishedTxtPathExists, isLogPathExists
        gc.collect()

    def filter(self, id_urls):
        finished_ids = []
        isFinishedIdPathExists = os.path.exists(self.finished_id_path)
        if isFinishedIdPathExists is True:
            finished_ids = self.file.readFromCSV(self.finished_id_path)
        new_urls = []
        for id_url in id_urls:
            if [str(id_url[0]).replace('\xef\xbb\xbf','')] not in finished_ids:
                new_urls.append(id_url[1])
        del finished_ids, isFinishedIdPathExists
        gc.collect()
        return new_urls

    def readNewUrls(self):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(self.url_path)
        new_urls = []
        if isUrlPathExit is True:
            id_urls = np.array(self.file.readColsFromCSV(self.url_path, ['id', 'url']))
            new_urls = self.filter(id_urls)
        del isUrlPathExit
        gc.collect()
        return new_urls

    def storeFinishedId(self, id):
        print 'Start to store finished id: {0}'.format(id)
        self.file.writeToCSVWithoutHeader(self.finished_id_path, [id])
        self.file.logger(self.log_path, 'End to store finished id: {0}'.format(id))
        print 'End to store finished id: {0}'.format(id)

    def storeMongodb(self, data):
        print 'Start to store mongo: {0}'.format(data['url'])
        mongo = MongoMiddleware()
        mongo.insert(self.mongo, data)
        print 'End to store mongo: {0}'.format(data['url'])
        self.storeFinishedId(data['id'])
        del mongo
        gc.collect()

    def storeTxt(self, id, content):
        print 'Start to store txt: {0}'.format(id)
        self.file.writeToTxtCover('{0}//{1}_{2}.txt'.format(self.finished_txt_path, self.name, id), content)
        print 'End to store txt: {0}'.format(id)

    def isEmpty(self, item_list):
        return len([item for item in item_list if item.strip()]) == 0

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            short_url_parts = re.split(r'[., /, _]',  response['request_url'])
            invalid_id = short_url_parts[short_url_parts.index('r') + 1]
            self.storeFinishedId(invalid_id)
            self.file.logger(self.log_path, 'Invalid url: {0}'.format(current_url))
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _, #]', current_url)
        current_id = short_url_parts[len(short_url_parts) - 2]
        html = etree.HTML(response['response'].page_source)
        article_0 = html.xpath(".//*[contains(@class, 'content')]/text()")
        data = {}
        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(article_0) > 0:
            title0_1 = html.xpath(".//article/h1/text()")
            author_name0_1 = html.xpath(".//*[contains(@class, 'time')]/span/text()")
            time0_1 = html.xpath(".//*[contains(@class, 'time')]/span/text()")
            content0_1 = html.xpath(".//div[contains(@class, 'content')]/p/text()")

            url = current_url
            id = current_id
            if self.isEmpty(content0_1) is False:
                content = ''.join(content0_1).strip()
            if self.isEmpty(time0_1) is False:
                time = time0_1[0].strip()
            if self.isEmpty(author_name0_1) is False:
                author_name = author_name0_1[1].strip()
            if self.isEmpty(title0_1) is False:
                title = title0_1[0].strip()

            data = {
                'url': url,
                'time': time,
                'author_name': author_name,
                'title': title,
                'id': id
            }


        print 'End to parse: {0}'.format(current_url)
        if len(data) == 0:
            self.storeFinishedId(current_id)
        else:
            self.storeMongodb(data)
            self.storeTxt(id, content)

        del current_url, valid,  current_id, html, data
        gc.collect()

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start requests: {0} '.format(self.name))
        print 'Start requests: {0} '.format(self.name)
        new_urls = self.readNewUrls()
        # new_urls = ["http://www.eeo.com.cn/2018/1218/343618.shtml"]
        if len(new_urls) == 0:
            self.file.logger(self.log_path, 'No new url for {0}'.format(self.name))
            print 'No new url for {0}'.format(self.name)
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End requests for {0}'.format(str(len(content))))
        print 'End requests for {0}'.format(str(len(content)))
        del content, new_urls, request
        gc.collect()

if __name__ == '__main__':
    cankaoxiaoxi=Cankaoxiaoxi()
    cankaoxiaoxi.start_requests()