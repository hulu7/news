#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
from lxml import etree
import gc
import time
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class CamelBone():

    def __init__(self, siteinfo=None, callback=callable):
        self.siteinfo = siteinfo
        self.callBack = callback
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.log_path)

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings(self.siteinfo)
        self.log_path = self.globalSettings.LOG_PATH_PRD2
        self.today = self.globalSettings.TODAY
        self.source = self.settings.SOURCE_NAME
        self.work_path_prd2 = self.settings.WORK_PATH_PRD2
        self.mongo = self.settings.MONGO_URLS
        self.name = self.settings.NAME
        self.max_pool_size = self.settings.MAX_POOL_SIZE_URL
        self.urls = self.settings.URLS
        self.max_concurrency = self.globalSettings.MAX_CONCURRENCY
        self.concurrency_file = self.globalSettings.CONCURRENCY_FILE

    def parse(self, response):
        time.sleep(1)
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        results = self.callBack(current_url, html)
        if len(results) == 0:
            message1 = 'No url for page: {0}'.format(current_url)
            self.file.logger(self.log_path, message1)
            print message1
        for item in results:
            is_title_empty = self.doraemon.isEmpty(item.title)
            if (is_title_empty is False) and (self.doraemon.isDuplicated(self.doraemon.bf_urls, item.title) is False):
                message2 = 'Start to store mongo {0}'.format(item.url)
                self.file.logger(self.log_path, message2)
                print message2
                self.doraemon.storeMongodb(self.mongo, self.doraemon.createCamelMongoJson(item))
                message3 = 'End to store mongo {0}'.format(item.url)
                self.file.logger(self.log_path, message3)
                print message3
                self.file.logger(self.log_path, 'Done for {0}'.format(item.url))
            else:
                if is_title_empty is True:
                    message4 = 'Empty title for {0}'.format(item.url)
                    self.file.logger(self.log_path, message4)
                    print message4
                else:
                    print 'Finished title for {0}'.format(item.url)
        print 'End to parse {0}'.format(current_url)

        del current_url, results, html
        gc.collect()

    def start(self):
        if self.doraemon.isCamelReadyToRun(self.settings) is False:
            message5 = 'It is not ready to run for {0}'.format(self.name)
            print message5
            return
        message6 = 'Start {0} requests'.format(self.name)
        self.file.logger(self.log_path, message6)
        print message6

        new_urls = []
        content = self.file.readFromTxt(self.urls)
        url_list = content.split('\n')

        for url in url_list:
            if self.doraemon.isEmpty(url) is False:
                new_urls.append([url, ''])

        if len(new_urls) == 0:
            print 'No url.'
            return
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.doraemon.recoveryConcurrency(self.concurrency_file, self.max_concurrency)
        message7 = 'End for {0} requests of {1}.'.format(str(len(content)), self.name)
        self.file.logger(self.log_path, message7)
        print message7

        del new_urls, content, url_list, request
        gc.collect()

if __name__ == '__main__':
    camelBone=CamelBone()
    camelBone.start()