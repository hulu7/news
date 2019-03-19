# -*- coding: utf-8 -*-
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import re
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Ifeng():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd1 = Settings.IFENG['WORK_PATH_PRD1']
        self.finished_txt_path = Settings.IFENG['FINISHED_TXT_PATH']
        self.url_path = Settings.IFENG['URL_PATH']
        self.mongo = Settings.IFENG['MONGO']
        self.name = Settings.IFENG['NAME']
        self.max_pool_size = Settings.IFENG['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH
        self.today = Settings.TODAY
        self.is_open_cache = Settings.IFENG['IS_OPEN_CACHE']

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        request_url = response['request_url'].encode('gbk')
        if self.doraemon.isEmpty(current_url):
            return
        url_parts = re.split(r'[., /, _, #]', current_url)
        for key in self.badkeys:
            if key in current_url:
                self.file.logger(self.log_path, 'Bad url: {0}'.format(request_url))
                print 'Bad url: {0}'.format(request_url)
                self.doraemon.storeFinished(response['request_title'])
                del current_url
                return

        current_id = ""
        hasId = False
        if ('/c/' in current_url) and (hasId is False):
            id_index = url_parts.index('c') + 1
            current_id = url_parts[id_index].strip()
            hasId = True
        if ('news' in current_url) and (hasId is False):
            id_index = url_parts.index('ifeng') + 2
            current_id = url_parts[id_index].strip()
            hasId = True
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
            article_6 = html.xpath(".//*[contains(@class, 'acTxtTit wrap_w94')]")
            if len(article_0) > 0:
                comment_number0_1 = html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")
                join_number0_1 = html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")
                content0_1 = html.xpath(".//div[@id='main_content']/p/text()")
                time0_1 = html.xpath(".//*[contains(@class, 'ss01')]/text()")
                time0_2 = html.xpath(".//*[@id='artical_sth']/p/span/text()")
                author_name0_1 = self.name
                author_name0_2 = self.name
                author_name0_3 = self.name
                title0_1 = html.xpath(".//*[@id='artical_topic']/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number0_1) is False:
                    comment_number = str(filter(str.isdigit, str(comment_number0_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(join_number0_1) is False:
                    join_number = str(filter(str.isdigit, str(join_number0_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.doraemon.isEmpty(time0_1) is False:
                    time = time0_1[0].strip()
                if self.doraemon.isEmpty(time0_2) is False:
                    time = time0_2[0].strip()
                if self.doraemon.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1
                if self.doraemon.isEmpty(author_name0_2) is False:
                    author_name = author_name0_2
                if self.doraemon.isEmpty(author_name0_3) is False:
                    author_name = author_name0_3
                if self.doraemon.isEmpty(title0_1) is False:
                    title = title0_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            if len(article_1) > 0:
                comment_number1_1 = html.xpath(".//*[contains(@class, 'js_cmtNum')]//text()")
                join_number1_1 = html.xpath(".//*[contains(@class, 'js_joinNum')]//text()")
                content1_1 = html.xpath(".//div[@id='yc_con_txt']/p/text()")
                time1_1 = html.xpath(".//*[contains(@class, 'yc_tit')]//p//span/text()")
                author_name1_1 = self.name
                title1_1 = html.xpath(".//*[contains(@class, 'yc_tit')]//h1/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number1_1) is False:
                    comment_number = str(filter(str.isdigit,comment_number1_1[0].encode('gbk'))).strip()
                if self.doraemon.isEmpty(join_number1_1) is False:
                    join_number = str(filter(str.isdigit, join_number1_1[0].encode('gbk'))).strip()
                if self.doraemon.isEmpty(content1_1) is False:
                    content = ''.join(content1_1).strip()
                if self.doraemon.isEmpty(time1_1) is False:
                    time = time1_1[0].strip()
                if self.doraemon.isEmpty(author_name1_1) is False:
                    author_name = author_name1_1
                if self.doraemon.isEmpty(title1_1) is False:
                    title = title1_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            if len(article_2) > 0:
                comment_number2_1 = html.xpath(".//*[contains(@class, 'w-com')]//text()")
                join_number2_1 = html.xpath(".//*[contains(@class, 'w-reply')]//text()")
                content2_1 = html.xpath(".//div[contains(@class, 'articleContent')]/p/text()")
                time2_1 = html.xpath(".//*[contains(@class, 'time01')]//text()")
                author_name2_1 = self.name
                title2_1 = html.xpath(".//*[contains(@class, 'tit01')]//a/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number2_1) is False:
                    comment_number = str(filter(str.isdigit, comment_number2_1)).strip()
                if self.doraemon.isEmpty(join_number2_1) is False:
                    join_number = str(filter(str.isdigit, str(join_number2_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(content2_1) is False:
                    content = ''.join(content2_1)
                if self.doraemon.isEmpty(time2_1) is False:
                    time = time2_1[0].strip()
                if self.doraemon.isEmpty(author_name2_1) is False:
                    author_name = author_name2_1
                if self.doraemon.isEmpty(title2_1) is False:
                    title = title2_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            if len(article_3) > 0:
                comment_number3_1 = html.xpath(".//*[contains(@class, 'num-1eBOY5Jv')]//text()")
                join_number3_1 = html.xpath(".//*[contains(@class, 'num-1eBOY5Jv')]//text()")
                content3_1 = html.xpath(".//div[contains(@class, 'text-3zQ3cZD4')]/p/text()")
                time3_1 = html.xpath(".//*[contains(@class, 'time-hm3v7ddj')]/span/text()")
                author_name3_1 = self.name
                title3_1 = html.xpath(".//*[contains(@class, 'topic-3bY8Hw-9')]//text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number3_1) is False:
                    comment_number = str(filter(str.isdigit, str(comment_number3_1[1]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(join_number3_1) is False:
                    join_number = str(filter(str.isdigit, str(join_number3_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(content3_1) is False:
                    content = ''.join(content3_1)
                if self.doraemon.isEmpty(time3_1) is False:
                    time = time3_1[0].strip()
                if self.doraemon.isEmpty(author_name3_1) is False:
                    author_name = author_name3_1
                if self.doraemon.isEmpty(title3_1) is False:
                    title = title3_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            if len(article_4) > 0:
                comment_number4_1 = html.xpath(".//*[contains(@class, 'comments')]/a/strong/text()")
                join_number4_1 = html.xpath(".//*[contains(@class, 'peoples')]/a/strong/text()")
                content4_1 = html.xpath(".//div[contains(@class, 'article')]/p/text()")
                time4_1 = html.xpath(".//*[contains(@class, 'marb-5')]/span/text()")
                author_name4_1 = self.name
                title4_1 = html.xpath(".//*[contains(@class, 'title')]/h2/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number4_1) is False:
                    comment_number = str(filter(str.isdigit, str(comment_number4_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(join_number4_1) is False:
                    join_number = str(filter(str.isdigit, str(join_number4_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(content4_1) is False:
                    content = ''.join(content4_1)
                if self.doraemon.isEmpty(time4_1) is False:
                    time = time4_1[0].strip()
                if self.doraemon.isEmpty(author_name4_1) is False:
                    author_name = author_name4_1
                if self.doraemon.isEmpty(title4_1) is False:
                    title = title4_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            if len(article_5) > 0:
                comment_number5_1 = html.xpath(".//*[contains(@class, 'w-num')]//text()")
                join_number5_1 = html.xpath(".//*[contains(@class, 'w-num')]//text()")
                content5_1 = html.xpath(".//div[contains(@class, 'artical-main')]/p/text()")
                time5_1 = html.xpath(".//*[contains(@class, 'artical-source')]//text()")
                author_name5_1 = self.name
                title5_1 = html.xpath(".//*[contains(@class, 'w90 artical')]/h1/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number5_1) is False:
                    comment_number = str(filter(str.isdigit, str(comment_number5_1[1]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(join_number5_1) is False:
                    join_number = str(filter(str.isdigit, str(join_number5_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(content5_1) is False:
                    content = ''.join(content5_1)
                if self.doraemon.isEmpty(time5_1) is False:
                    time = time5_1[0].strip()
                if self.doraemon.isEmpty(author_name5_1) is False:
                    author_name = author_name5_1
                if self.doraemon.isEmpty(title5_1) is False:
                    title = title5_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            if len(article_6) > 0:
                comment_number6_1 = html.xpath(".//*[contains(@class, 'w-num')]/text()")
                join_number6_1 = html.xpath(".//*[contains(@class, 'w-num')]/text()")
                content6_1 = html.xpath(".//div[contains(@class, 'acTx')]/p/text()")
                time6_1 = html.xpath(".//*[contains(@class, 'acTxtTit wrap_w94')]/div/div/span/text()")
                author_name6_1 = self.name
                title6_1 = html.xpath(".//*[contains(@class, 'acTxtTit wrap_w94')]/h1/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(comment_number6_1) is False:
                    comment_number = str(filter(str.isdigit, str(comment_number6_1[1]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(join_number6_1) is False:
                    join_number = str(filter(str.isdigit, str(join_number6_1[0]).encode('gbk'))).strip()
                if self.doraemon.isEmpty(content6_1) is False:
                    content = ''.join(content6_1)
                if self.doraemon.isEmpty(time6_1) is False:
                    time = '{0} {1}'.format(time6_1[0], time6_1[1]).strip()
                if self.doraemon.isEmpty(author_name6_1) is False:
                    author_name = author_name6_1
                if self.doraemon.isEmpty(title6_1) is False:
                    title = title6_1[0].strip()

                data = {
                    'comment_number': comment_number,
                    'join_number': join_number,
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today,
                    'is_open_cache': self.is_open_cache
                }

            print 'End to parse: {0}'.format(current_url)
            if len(data) == 0:
                print 'Empty data: {0}'.format(request_url)
                self.doraemon.storeFinished(response['request_title'])
            else:
                self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
                print 'Start to store mongo {0}'.format(data['url'])
                self.doraemon.storeMongodb(self.mongo, data)
                self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
                print 'End to store mongo {0}'.format(data['url'])
                self.doraemon.storeTxt(id, content, self.finished_txt_path, self.name)
                self.doraemon.storeFinished(response['request_title'])

    def start_requests(self):
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        self.badkeys = ['#p', 'junjichu', '404', '/NaN/']
        new_url_titles = self.doraemon.readNewUrls(self.url_path)
        if len(new_url_titles) == 0:
            self.file.logger(self.log_path, 'No new url for: {0}'.format(self.name))
            print 'No new url for: {0}'.format(self.name)
            return
        request = BrowserRequest()
        content = request.start_chrome(new_url_titles, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End requests: {0}'.format(str(len(content))))
        print 'End requests: {0}'.format(str(len(content)))

if __name__ == '__main__':
    ifeng=Ifeng()
    ifeng.start_requests()