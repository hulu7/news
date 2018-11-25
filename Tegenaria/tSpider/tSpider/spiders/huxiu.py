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

    def filter(self, id_urls):
        finished_ids = []
        isFinishedIdPathExists = os.path.exists(self.finished_id_path)
        if isFinishedIdPathExists is True:
            finished_ids = self.file.readFromCSV(self.finished_id_path)
        new_urls = []
        for id_url in id_urls:
            if [str(id_url[0]).replace('\xef\xbb\xbf','')] not in finished_ids:
                new_urls.append(id_url[1])
        return new_urls

    def readNewUrls(self):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(self.url_path)
        new_urls = []
        if isUrlPathExit is True:
            id_urls = np.array(self.file.readColsFromCSV(self.url_path, ['id', 'url']))
            new_urls = self.filter(id_urls)
        return new_urls

    def storeFinishedId(self, id):
        print 'Start to store finished id %s' % id
        self.file.writeToCSVWithoutHeader(self.finished_id_path, [id.replace('\xef\xbb\xbf','')])
        print 'End to store finished id %s' % id

    def storeMongodb(self, data):
        print 'Start to store mongo %s' % data['url']
        mongo = MongoMiddleware()
        mongo.insert( self.mongo, data)
        print 'End to store mongo %s' % data['url']

    def storeTxt(self, id, content):
        print 'Start to store txt %s' % id
        self.file.writeToTxtCover(self.finished_txt_path + '//' + self.name + '_' + id + '.txt', content)
        print 'End to store txt %s' % id
        self.storeFinishedId(id)

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse %s' % current_url
        html = etree.HTML(response['response'].page_source)
        title = html.xpath(".//*[contains(@class,'t-h1')]/text()")[0].strip()
        comment_number = str(
            filter(str.isdigit, html.xpath(".//*[contains(@class, 'article-pl pull-left')]/text()")[0].encode('gbk')))
        share_number = str(filter(str.isdigit,
                                  html.xpath(".//*[contains(@class, 'article-share pull-left')]/text()")[0].encode(
                                      'gbk')))
        image_url = html.xpath(".//*[contains(@class, 'article-img-box')]/img/@src")[0]
        url = current_url
        content = ''.join(html.xpath(".//div[contains(@class, 'article-content-wrap')]/p/text()"))
        time = html.xpath(".//*[@class='article-time pull-left']/text()")[0]
        author_url = urlparse.urljoin(current_url, html.xpath(".//*[@class='author-name']/a/@href")[0])
        author_name = html.xpath(".//*[@class='author-name']/a/text()")[0]
        id = str(filter(str.isdigit, current_url.encode('gbk')))
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
        print 'End to parse %s' % current_url

        self.storeMongodb(data)
        self.storeTxt(id, content)

    def start_requests(self, urls):
        self.init()
        self.file.logger(self.log_path, 'Start '+ self.name +' requests')
        print 'Start ' + self.name + ' requests'
        new_urls = self.readNewUrls()
        if len(new_urls) == 0:
            self.file.logger(self.log_path, 'No new url for ' + self.name + ' and return')
            print 'No new url for ' + self.name + ' and return'
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, callback=self.parse)
        self.file.logger(self.log_path, 'End %s requests' % str(len(content)))
        print 'End %s requests' % str(len(content))

if __name__ == '__main__':
    huxiu=Huxiu()
    urls = ['https://www.huxiu.com/article/273257.html', 'https://www.huxiu.com/article/273262.html']
    huxiu.start_requests(urls)