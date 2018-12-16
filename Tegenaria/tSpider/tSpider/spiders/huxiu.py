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
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class Huxiu():
    def getSettings(self):
        self.work_path_prd1 = Settings.HUXIU['WORK_PATH_PRD1']
        self.finished_txt_path = Settings.HUXIU['FINISHED_TXT_PATH']
        self.finished_id_path = Settings.HUXIU['FINISHED_ID_PATH']
        self.url_path = Settings.HUXIU['URL_PATH']
        self.mongo = Settings.HUXIU['MONGO']
        self.name = Settings.HUXIU['NAME']
        self.max_pool_size = Settings.HUXIU['MAX_POOL_SIZE']
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
        self.file.writeToCSVWithoutHeader(self.finished_id_path, [id.replace('\xef\xbb\xbf','')])
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
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        data = {}
        comment_number = ""
        title = ""
        url = ""
        id = ""
        share_number = ""
        image_url = ""
        content = ""
        time = ""
        author_url = ""
        author_name = ""
        valid = False

        url = current_url
        id = str(filter(str.isdigit, current_url.encode('gbk')))
        title1 = html.xpath(".//*[contains(@class,'t-h1')]/text()")
        comment_number1 = html.xpath(".//*[contains(@class, 'article-pl pull-left')]/text()")
        share_number1 = html.xpath(".//*[contains(@class, 'article-share pull-left')]/text()")
        image_url1 = html.xpath(".//*[contains(@class, 'article-img-box')]/img/@src")
        content1 = html.xpath(".//div[contains(@class, 'article-content-wrap')]/p/text()")
        time1 = html.xpath(".//*[@class='article-time pull-left']/text()")
        author_url1 = html.xpath(".//*[@class='author-name']/a/@href")
        author_name1 = html.xpath(".//*[@class='author-name']/a/text()")

        if self.isEmpty(title1) is False:
            title = title1[0].strip()
        if self.isEmpty(comment_number1) is False:
            comment_number = str(filter(str.isdigit, comment_number1[0].encode('gbk'))).strip()
        if self.isEmpty(share_number1) is False:
            share_number = str(filter(str.isdigit, share_number1[0].encode('gbk'))).strip()
        if self.isEmpty(image_url1) is False:
            image_url = image_url1[0].strip()
        if self.isEmpty(content1) is False:
            content = ''.join(content1).strip()
            valid = True
        if self.isEmpty(time1) is False:
            time = time1[0]
        if self.isEmpty(author_url1) is False:
            author_url = urlparse.urljoin(current_url, author_url1[0].strip())
        if self.isEmpty(author_name1) is False:
            author_name = author_name1[0].strip()

        data = {
            'title': title,
            'comment_number': comment_number,
            'share_number': share_number,
            'image_url': image_url,
            'url': url,
            'time': time,
            'author_url': author_url,
            'author_name': author_name,
            'id': id
        }
        print 'End to parse: {0}'.format(current_url)
        if valid == True:
            self.storeMongodb(data)
            self.storeTxt(id, content)
        else:
            self.storeFinishedId(id)
        del current_url, html, title, comment_number, share_number, image_url, url, content, time, author_url, author_name, id, data
        gc.collect()

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start ' + self.name + ' requests'
        new_urls = self.readNewUrls()
        if len(new_urls) == 0:
            self.file.logger(self.log_path, 'No new url for: {0}'.format(self.name))
            print 'No new url for: {0}'.format(self.name)
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End requests: {0}'.format(str(len(content))))
        print 'End requests: {0}'.format(str(len(content)))
        del new_urls, request, content
        gc.collect()

if __name__ == '__main__':
    huxiu=Huxiu()
    huxiu.start_requests()