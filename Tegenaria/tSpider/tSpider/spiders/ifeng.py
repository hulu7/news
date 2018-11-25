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
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class Ifeng():
    def getSettings(self):
        self.work_path_prd1 = Settings.IFENG['WORK_PATH_PRD1']
        self.finished_txt_path = Settings.IFENG['FINISHED_TXT_PATH']
        self.finished_id_path = Settings.IFENG['FINISHED_ID_PATH']
        self.url_path = Settings.IFENG['URL_PATH']
        self.mongo = Settings.IFENG['MONGO']
        self.name = Settings.IFENG['NAME']
        self.max_pool_size = Settings.IFENG['MAX_POOL_SIZE']
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
            if [str(id_url[1]).replace('\xef\xbb\xbf','')] not in finished_ids:
                new_urls.append(id_url[0])
        return new_urls

    def readNewUrls(self):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(self.url_path)
        new_urls = []
        if isUrlPathExit is True:
            id_urls = np.array(self.file.readColsFromCSV(self.url_path, ['content.id', 'content.docUrl']))
            new_urls = self.filter(id_urls)
        return new_urls

    def storeFinishedId(self, id):
        print 'Start to store finished id %s' % id
        self.file.writeToCSVWithoutHeader(self.finished_id_path, [id])
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
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            invalid_id = re.split('_', re.split('/', response['request_url'])[5])[0]
            self.storeFinishedId(invalid_id)
            self.file.logger(self.log_path, 'Invalid url')
            print 'Invalid url'
            return
        print 'Start to parse %s' % current_url
        current_id = re.split('_', re.split('/', current_url)[5])[0]
        html = etree.HTML(response['response'].page_source)
        not_fnd = html.xpath(".//*[contains(@class,'tips404')]/text()")
        data={}
        if len(not_fnd) != 1:
            article_0 = html.xpath(".//*[@id='artical']")
            article_1 = html.xpath(".//*[contains(@class, 'yc_main wrap')]")
            article_2 = html.xpath(".//*[contains(@class, 'col01')]")
            if len(article_0) > 0:
                comment_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")[0].encode('gbk')))
                join_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'js_joinNum')]//text()")[0].encode('gbk')))
                url = current_url
                content = ''.join(html.xpath(".//div[@id='main_content']/p/text()"))
                time = html.xpath(".//*[@class='ss01']/text()")[0]
                author_name = html.xpath(".//*[contains(@class, 'ss03')]//text()")[0]
                title = html.xpath(".//*[@id='artical_topic']/text()")[0]
                id = current_id

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id
                }

            if len(article_1) > 0:
                comment_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")[0].encode('gbk')))
                join_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'js_joinNum')]//text()")[0].encode('gbk')))
                url = current_url
                content = ''.join(html.xpath(".//div[@id='yc_con_txt']/p/text()"))
                time = html.xpath(".//*[contains(@class, 'yc_tit')]//p//span/text()")[0]
                author_name = html.xpath(".//*[contains(@class, 'yc_tit')]//p//a/text()")[0]
                title = html.xpath(".//*[contains(@class, 'yc_tit')]//h1/text()")[0]
                id = current_id

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id
                }

            if len(article_2) > 0:
                comment_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'w-com')]//text()")[0].encode('gbk')))
                join_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'w-reply')]//text()")[0].encode('gbk')))
                url = current_url
                content = ''.join(html.xpath(".//div[contains(@class, 'articleContent')]/p/text()"))
                time = html.xpath(".//*[contains(@class, 'time01')]//text()")[0]
                author_name = ''.join(html.xpath(".//*[contains(@class, 'cmtNav js_crumb')]//a/text()"))
                title = html.xpath(".//*[contains(@class, 'tit01')]//a/text()")[0]
                id = current_id

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id
                }

            print 'End to parse %s' % current_url

            if len(data) != 0:
                self.storeMongodb(data)
                self.storeTxt(id, content)


    def start_requests(self, urls):
        self.init()
        self.file.logger(self.log_path, 'Start '+ self.name +' requests')
        print 'Start ' + self.name + ' requests'
        new_urls = self.readNewUrls()
        # new_urls = urls
        if len(new_urls) == 0:
            self.file.logger(self.log_path, 'No new url for ' + self.name + ' and return')
            print 'No new url for ' + self.name + ' and return'
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, callback=self.parse)
        self.file.logger(self.log_path, 'End %s requests' % str(len(content)))
        print 'End %s requests' % str(len(content))

if __name__ == '__main__':
    ifeng=Ifeng()
    urls = ['http://sports.ifeng.com/a/20180725/59401930_0.shtml']
    ifeng.start_requests(urls)