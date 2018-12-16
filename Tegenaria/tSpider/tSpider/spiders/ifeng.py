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
            id = str(id_url[0])
            url = str(id_url[1])
            if [id.replace('\xef\xbb\xbf','')] not in finished_ids:
                    new_urls.append(url)
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
        request_url = response['request_url'].encode('gbk')
        if self.isEmpty(current_url):
            return
        url_parts = re.split(r'[., /, _, #]', current_url)
        for key in self.badkeys:
            if key in current_url:
                self.file.logger(self.log_path, 'Bad url: {0}'.format(request_url))
                print 'Bad url: {0}'.format(request_url)
                url_parts = re.split(r'[., /, _]', request_url)
                if '/c/' in request_url:
                    id_index = url_parts.index('c') + 1
                    request_id = url_parts[id_index].strip()
                if '/a/' in request_url:
                    id_index = url_parts.index('a') + 2
                    request_id = url_parts[id_index].strip()
                if 'detail' in request_url:
                    id_index = url_parts.index('detail') + 4
                    request_id = url_parts[id_index].strip()
                self.storeFinishedId(str(request_id))
                del current_url, request_url
                return

        current_id = ""
        if '/c/' in current_url:
            id_index = url_parts.index('c') + 1
            current_id = url_parts[id_index].strip()
        if '/a/' in current_url:
            id_index = url_parts.index('a') + 2
            current_id = url_parts[id_index].strip()
        if 'detail' in current_url:
            id_index = url_parts.index('detail') + 4
            current_id = url_parts[id_index].strip()
        print 'Start to parse: {0} with id: {1}'.format(current_url, current_id)
        html = etree.HTML(response['response'].page_source)
        not_fnd = html.xpath(".//*[contains(@class,'tips404')]/text()")
        data = {}
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
            article_3 = html.xpath(".//*[contains(@class, 'artical-_Qk9Dp2t')]")
            article_4 = html.xpath(".//*[contains(@class, 'wdetailbox ctltbox')]")
            article_5 = html.xpath(".//*[contains(@class, 'w90 artical')]")
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

            if len(article_3) > 0:
                comment_number3_1 = html.xpath(".//*[contains(@class, 'num-1eBOY5Jv')]//text()")
                join_number3_1 = html.xpath(".//*[contains(@class, 'num-1eBOY5Jv')]//text()")
                content3_1 = html.xpath(".//div[contains(@class, 'text-3zQ3cZD4')]/p/text()")
                time3_1 = html.xpath(".//*[contains(@class, 'time-hm3v7ddj')]/span/text()")
                author_name3_1 = html.xpath(".//*[contains(@class, 'source-2pXi2vGI')]/span/text()")
                title3_1 = html.xpath(".//*[contains(@class, 'topic-3bY8Hw-9')]//text()")

                url = current_url
                id = current_id
                if self.isEmpty(comment_number3_1) is False:
                    comment_number = str(filter(str.isdigit, comment_number3_1[1].encode('gbk'))).strip()
                if self.isEmpty(join_number3_1) is False:
                    join_number = str(filter(str.isdigit, join_number3_1[0].encode('gbk'))).strip()
                if self.isEmpty(content3_1) is False:
                    content = ''.join(content3_1)
                if self.isEmpty(time3_1) is False:
                    time = time3_1[0].strip()
                if self.isEmpty(author_name3_1) is False:
                    author_name = ''.join(author_name3_1).strip()
                if self.isEmpty(title3_1) is False:
                    title = title3_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id
                }

            if len(article_4) > 0:
                comment_number4_1 = html.xpath(".//*[contains(@class, 'comments')]/a/strong/text()")
                join_number4_1 = html.xpath(".//*[contains(@class, 'peoples')]/a/strong/text()")
                content4_1 = html.xpath(".//div[contains(@class, 'article')]/p/text()")
                time4_1 = html.xpath(".//*[contains(@class, 'marb-5')]/span/text()")
                author_name4_1 = html.xpath(".//*[contains(@class, 'pr')]/span/text()")
                title4_1 = html.xpath(".//*[contains(@class, 'title')]/h2/text()")

                url = current_url
                id = current_id
                if self.isEmpty(comment_number4_1) is False:
                    comment_number = str(filter(str.isdigit, comment_number4_1[0].encode('gbk'))).strip()
                if self.isEmpty(join_number4_1) is False:
                    join_number = str(filter(str.isdigit, join_number4_1[0].encode('gbk'))).strip()
                if self.isEmpty(content4_1) is False:
                    content = ''.join(content4_1)
                if self.isEmpty(time4_1) is False:
                    time = time4_1[0].strip()
                if self.isEmpty(author_name4_1) is False:
                    author_name = ''.join(author_name4_1).strip()
                if self.isEmpty(title4_1) is False:
                    title = title4_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id
                }

            if len(article_5) > 0:
                comment_number5_1 = html.xpath(".//*[contains(@class, 'w-num')]//text()")
                join_number5_1 = html.xpath(".//*[contains(@class, 'w-num')]//text()")
                content5_1 = html.xpath(".//div[contains(@class, 'artical-main')]/p/text()")
                time5_1 = html.xpath(".//*[contains(@class, 'artical-source')]//text()")
                author_name5_1 = html.xpath(".//*[contains(@class, 'artical-time')]//text()")
                title5_1 = html.xpath(".//*[contains(@class, 'w90 artical')]/h1/text()")

                url = current_url
                id = current_id
                if self.isEmpty(comment_number5_1) is False:
                    comment_number = str(filter(str.isdigit, comment_number5_1[1].encode('gbk'))).strip()
                if self.isEmpty(join_number5_1) is False:
                    join_number = str(filter(str.isdigit, join_number5_1[0].encode('gbk'))).strip()
                if self.isEmpty(content5_1) is False:
                    content = ''.join(content5_1)
                if self.isEmpty(time5_1) is False:
                    time = time5_1[0].strip()
                if self.isEmpty(author_name5_1) is False:
                    author_name = ''.join(author_name5_1).strip()
                if self.isEmpty(title5_1) is False:
                    title = title5_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
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
        del current_url, current_id, html, not_fnd, data
        gc.collect()

    def start_requests(self):
        self.init()
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        self.badkeys = ['#p', 'junjichu']
        new_urls = self.readNewUrls()
        # new_urls = ["https://ihouse.ifeng.com/detail/2018_12_12/51784060_0.shtml"]
        if len(new_urls) == 0:
            self.file.logger(self.log_path, 'No new url for: {0}'.format(self.name))
            print 'No new url for: {0}'.format(self.name)
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End requests: {0}'.format(str(len(content))))
        print 'End requests: {0}'.format(str(len(content)))
        del content, new_urls, request
        gc.collect()

if __name__ == '__main__':
    ifeng=Ifeng()
    ifeng.start_requests()