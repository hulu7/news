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
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Chuansongme():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd1 = Settings.CHUANSONGME['WORK_PATH_PRD1']
        self.finished_txt_path = Settings.CHUANSONGME['FINISHED_TXT_PATH']
        self.url_path = Settings.CHUANSONGME['URL_PATH']
        self.mongo = Settings.CHUANSONGME['MONGO']
        self.name = Settings.CHUANSONGME['NAME']
        self.max_pool_size = Settings.CHUANSONGME['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH
        self.today = Settings.TODAY

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            self.doraemon.storeFinished(response['request_title'])
            self.file.logger(self.log_path, 'Invalid url: {0}'.format(current_url))
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _]', current_url)
        current_id = short_url_parts[len(short_url_parts) - 1]
        html = etree.HTML(response['response'].page_source)
        content_found = html.xpath(".//*[contains(@class,'rich_media_inner')]")
        data = {}
        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(content_found) > 0:
            article_0 = html.xpath(".//*[contains(@class,'rich_media_inner')]")
            if len(article_0) > 0:
                content0_1 = html.xpath(".//*[contains(@class, 'rich_media_content ')]//text()")
                time0_1 = html.xpath(".//*[contains(@id, 'publish_time')]/text()")
                author_name0_1 = html.xpath(".//*[contains(@class, 'rich_media_meta rich_media_meta_nickname')]//text()")
                title0_1 = html.xpath(".//*[contains(@class,'rich_media_title')]/text()")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.doraemon.isEmpty(time0_1) is False:
                    time = time0_1[0].strip()
                if self.doraemon.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1[0].strip()
                if self.doraemon.isEmpty(title0_1) is False:
                    title = title0_1[0].strip()

                data = {
                    'url': url,
                    'time': time,
                    'author_name': author_name,
                    'title': title,
                    'id': id,
                    'download_time': self.today
                }

            print 'End to parse: {0}'.format(current_url)
            if len(data) == 0:
                self.doraemon.storeFinished(response['request_title'])
                print 'No data for {0}'.format(response['request_title'])
            else:
                self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
                print 'Start to store mongo {0}'.format(data['url'])
                self.doraemon.storeMongodb(self.mongo, data)
                self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
                print 'End to store mongo {0}'.format(data['url'])
                self.doraemon.storeTxt(id, content, self.finished_txt_path, self.name)
                self.doraemon.storeFinished(response['request_title'])

        del current_url, valid,  current_id, html, content_found, data
        gc.collect()

    def start_requests(self):
        self.file.logger(self.log_path, 'Start requests: {0} '.format(self.name))
        print 'Start requests: {0} '.format(self.name)
        new_url_titles = self.doraemon.readNewUrls(self.url_path)
        if len(new_url_titles) == 0:
            self.file.logger(self.log_path, 'No new url for {0}'.format(self.name))
            print 'No new url for {0}'.format(self.name)
            return
        request = BrowserRequest()
        content = request.start_chrome(new_url_titles, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End requests for {0}'.format(str(len(content))))
        print 'End requests for {0}'.format(str(len(content)))
        del content, new_url_titles, request
        gc.collect()

if __name__ == '__main__':
    chuansongme=Chuansongme()
    chuansongme.start_requests()