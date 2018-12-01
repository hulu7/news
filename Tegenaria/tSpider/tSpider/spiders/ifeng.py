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
from memory_profiler import profile
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
        del isWorkPathPrd1Exists, isFinishedTxtPathExists, isLogPathExists
        gc.collect()

    def filter(self, id_urls):
        finished_ids = []
        isFinishedIdPathExists = os.path.exists(self.finished_id_path)
        if isFinishedIdPathExists is True:
            finished_ids = self.file.readFromCSV(self.finished_id_path)
        new_urls = []
        for id_url in id_urls:
            if [str(id_url[1]).replace('\xef\xbb\xbf','')] not in finished_ids:
                if Settings.SETTINGS_IFENG not in str(id_url[0]):
                    self.storeFinishedId(str(id_url[1]).replace('\xef\xbb\xbf',''))
                    print 'Empty url with id: ' + str(id_url[1])
                    self.file.logger(self.log_path, 'Empty url with id: ' + str(id_url[1]))
                else:
                    new_urls.append(id_url[0])
        del finished_ids, isFinishedIdPathExists
        gc.collect()
        return new_urls

    def readNewUrls(self):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(self.url_path)
        new_urls = []
        if isUrlPathExit is True:
            id_urls = np.array(self.file.readColsFromCSV(self.url_path, ['content.id', 'content.docUrl']))
            new_urls = self.filter(id_urls)
        del isUrlPathExit
        gc.collect()
        return new_urls

    def storeFinishedId(self, id):
        print 'Start to store finished id %s' % id
        self.file.writeToCSVWithoutHeader(self.finished_id_path, [id])
        self.file.logger(self.log_path, 'End to store finished id %s' % id)
        print 'End to store finished id %s' % id

    def storeMongodb(self, data):
        print 'Start to store mongo %s' % data['url']
        mongo = MongoMiddleware()
        mongo.insert(self.mongo, data)
        del mongo
        gc.collect()
        print 'End to store mongo %s' % data['url']

    def storeTxt(self, id, content):
        print 'Start to store txt %s' % id
        self.file.writeToTxtCover(self.finished_txt_path + '//' + self.name + '_' + id + '.txt', content)
        print 'End to store txt %s' % id
        self.storeFinishedId(id)

    def isEmpty(self, item_list):
        return len([item for item in item_list if item.strip()]) == 0

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
        comment_number = ""
        join_number = ""
        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(not_fnd) != 1:
            article_0 = html.xpath(".//*[@id='artical']")
            article_1 = html.xpath(".//*[contains(@class, 'yc_main wrap')]")
            article_2 = html.xpath(".//*[contains(@class, 'col01')]")
            if len(article_0) > 0:
                comment_number0_1 = html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")
                join_number0_1 = html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")
                content0_1 = html.xpath(".//div[@id='main_content']/p/text()")
                time0_1 = html.xpath(".//*[contains(@class, 'ss01')]/text()")
                time0_2 = html.xpath(".//*[@id='artical_sth']/p/span/text()")
                author_name0_1 = html.xpath(".//*[contains(@class, 'ss03')]//text()")
                author_name0_2 = html.xpath(".//*[@id='artical_sth']/p/text()")
                author_name0_3 = html.xpath(".//*[@id='artical_sth']/p/span/span/a/text()")
                title0_1 = html.xpath(".//*[@id='artical_topic']/text()")

                url = current_url
                id = current_id
                if self.isEmpty(comment_number0_1) is False:
                    comment_number = str(filter(str.isdigit, comment_number0_1[0].encode('gbk'))).strip()
                if self.isEmpty(join_number0_1) is False:
                    join_number = str(filter(str.isdigit, join_number0_1[0].encode('gbk'))).strip()
                if self.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.isEmpty(time0_1) is False:
                    time = time0_1[0].strip()
                if self.isEmpty(time0_2) is False:
                    time = time0_2[0].strip()
                if self.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1[0].strip()
                if self.isEmpty(author_name0_2) is False:
                    author_name = author_name0_2[1].strip()
                if self.isEmpty(author_name0_3) is False:
                    author_name = author_name0_3[0].strip()
                if self.isEmpty(title0_1) is False:
                    title = title0_1[0].strip()

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
                comment_number1_1 = html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")
                join_number1_1 = html.xpath(".//*[contains(@class, 'js_joinNum')]//text()")
                content1_1 = html.xpath(".//div[@id='yc_con_txt']/p/text()")
                time1_1 = html.xpath(".//*[contains(@class, 'yc_tit')]//p//span/text()")
                author_name1_1 = html.xpath(".//*[contains(@class, 'yc_tit')]//p//a/text()")
                title1_1 = html.xpath(".//*[contains(@class, 'yc_tit')]//h1/text()")

                url = current_url
                id = current_id
                if self.isEmpty(comment_number1_1) is False:
                    comment_number = str(filter(str.isdigit,comment_number1_1[0].encode('gbk'))).strip()
                if self.isEmpty(join_number1_1) is False:
                    join_number = str(filter(str.isdigit, join_number1_1[0].encode('gbk'))).strip()
                if self.isEmpty(content1_1) is False:
                    content = ''.join(content1_1).strip()
                if self.isEmpty(time1_1) is False:
                    time = time1_1[0].strip()
                if self.isEmpty(author_name1_1) is False:
                    author_name = author_name1_1[0].strip()
                if self.isEmpty(title1_1) is False:
                    title = title1_1[0].strip()

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
                comment_number2_1 = html.xpath(".//*[contains(@class, 'w-com')]//text()")
                join_number2_1 = html.xpath(".//*[contains(@class, 'w-reply')]//text()")
                content2_1 = html.xpath(".//div[contains(@class, 'articleContent')]/p/text()")
                time2_1 = html.xpath(".//*[contains(@class, 'time01')]//text()")
                author_name2_1 = html.xpath(".//*[contains(@class, 'cmtNav js_crumb')]//a/text()")
                title2_1 = html.xpath(".//*[contains(@class, 'tit01')]//a/text()")

                url = current_url
                id = current_id
                if self.isEmpty(comment_number2_1) is False:
                    comment_number = str(filter(str.isdigit, comment_number2_1)).strip()
                if self.isEmpty(join_number2_1) is False:
                    join_number = str(filter(str.isdigit, join_number2_1[0].encode('gbk'))).strip()
                if self.isEmpty(content2_1) is False:
                    content = ''.join(content2_1)
                if self.isEmpty(time2_1) is False:
                    time = time2_1[0].strip()
                if self.isEmpty(author_name2_1) is False:
                    author_name = ''.join(author_name2_1).strip()
                if self.isEmpty(title2_1) is False:
                    title = title2_1[0].strip()

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
            if len(data) == 0:
                self.storeFinishedId(current_id)
            else:
                self.storeMongodb(data)
                self.storeTxt(id, content)
        del current_url, valid,  current_id, html, not_fnd, data
        gc.collect()

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start '+ self.name +' requests')
        print 'Start ' + self.name + ' requests'
        new_urls = self.readNewUrls()
        # new_urls = ["http://news.ifeng.com/a/20181122/60170554_0.shtml"]
        if len(new_urls) == 0:
            self.file.logger(self.log_path, 'No new url for ' + self.name + ' and return')
            print 'No new url for ' + self.name + ' and return'
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, callback=self.parse)
        self.file.logger(self.log_path, 'End %s requests' % str(len(content)))
        print 'End %s requests' % str(len(content))
        del content, new_urls, request
        gc.collect()

if __name__ == '__main__':
    ifeng=Ifeng()
    ifeng.start_requests()