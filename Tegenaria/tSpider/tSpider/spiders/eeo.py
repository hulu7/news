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

class Eeo():

    def __init__(self):
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(self.globalSettings.LOG_PATH)

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings('eeo')
        self.log_path = self.globalSettings.LOG_PATH
        self.today = self.globalSettings.TODAY

        self.source = self.settings.SOURCE_NAME
        self.work_path_prd1 = self.settings.WORK_PATH_PRD1
        self.finished_txt_path = self.settings.FINISHED_TXT_PATH
        self.url_path = self.settings.URL_PATH
        self.mongo = self.settings.MONGO
        self.name = self.settings.NAME
        self.max_pool_size = self.settings.MAX_POOL_SIZE
        self.is_open_cache = self.settings.IS_OPEN_CACHE


    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            self.doraemon.storeFinished(self.doraemon.bf_content, response['request_title'])
            self.file.logger(self.log_path, 'Invalid url: {0}'.format(current_url))
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _]', current_url)
        current_id = short_url_parts[len(short_url_parts) - 2]
        html = etree.HTML(response['response'].page_source)
        article_0 = html.xpath(".//*[contains(@class,'xd-b-left')]")
        data = {}
        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(article_0) > 0:
            content0_1 = html.xpath(".//div[contains(@class, 'xx_boxsing')]//p//text()")
            time0_1 = html.xpath(".//div[contains(@class, 'xd-b-b')]/p/span/text()")
            author_name0_1 = self.name
            title0_1 = html.xpath(".//*[contains(@class,'xd-b-b')]/h1/text()")
            images0_1 = html.xpath(".//*[contains(@class, 'xd-xd-xd-newsimg')]//img//@src")

            url = current_url
            id = current_id
            if self.doraemon.isEmpty(content0_1) is False:
                content = ''.join(content0_1).strip()
            if self.doraemon.isEmpty(time0_1) is False:
                time = ''.join(time0_1).strip()
                time = self.doraemon.getDateFromString(time)
            if self.doraemon.isEmpty(author_name0_1) is False:
                author_name = author_name0_1
            if self.doraemon.isEmpty(title0_1) is False:
                title = ''.join(title0_1).strip()

            images = []
            self.doraemon.updateImages(images, images0_1)

            data = self.doraemon.createSpidersData(url.strip(),
                                                   time.strip(),
                                                   author_name.strip(),
                                                   title.strip(),
                                                   id.strip(),
                                                   self.today,
                                                   self.source,
                                                   images,
                                                   self.is_open_cache)

        print 'End to parse: {0}'.format(current_url)
        if len(data) == 0:
            self.doraemon.storeFinished(self.doraemon.bf_content, response['request_title'])
        else:
            self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
            print 'Start to store mongo {0}'.format(data['url'])
            self.doraemon.storeMongodb(self.mongo, data)
            self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
            print 'End to store mongo {0}'.format(data['url'])
            self.doraemon.storeTxt(id, content, self.finished_txt_path, self.name)
            self.doraemon.storeFinished(self.doraemon.bf_content, response['request_title'])

        del current_url, valid,  current_id, html, data
        gc.collect()

    def start_requests(self):
        self.file.logger(self.log_path, 'Start requests: {0} '.format(self.name))
        print 'Start requests: {0} '.format(self.name)
        new_url_titles = self.doraemon.readNewUrls(self.doraemon.bf_content, self.url_path)
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
    eeo=Eeo()
    eeo.start_requests()