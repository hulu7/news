#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import gc
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class CamelBone():

    def __init__(self, settingName, callback=callable):
        self.settingName = settingName
        self.callBack = callback
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.globalSettings.LOG_PATH)

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings(self.settingName)
        self.log_path = self.globalSettings.LOG_PATH_PRD2
        self.today = self.globalSettings.TODAY
        self.source = self.settings.SOURCE_NAME
        self.work_path_prd2 = self.settings.WORK_PATH_PRD2
        self.mongo = self.settings.MONGO_URLS
        self.name = self.settings.NAME
        self.max_pool_size = self.settings.MAX_POOL_SIZE
        self.urls = self.settings.URLS


    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        results = self.callBack(current_url, html)
        if len(results) == 0:
            self.file.logger(self.log_path, 'No url for page: {0}'.format(current_url))
            print 'No url for page: {0}'.format(current_url)
        for item in results:
            is_title_empty = self.doraemon.isEmpty(item.title)
            if (is_title_empty is False) and (self.doraemon.isDuplicated(self.doraemon.bf_urls, item.title) is False):
                self.file.logger(self.log_path, 'Start to store mongo {0}'.format(item.url))
                print 'Start to store mongo {0}'.format(item.url)
                self.doraemon.storeMongodb(self.mongo, self.doraemon.createCamelMongoJson(item))
                self.file.logger(self.log_path, 'End to store mongo {0}'.format(item.url))
                print 'End to store mongo {0}'.format(item.url)
                self.file.logger(self.log_path, 'Done for {0}'.format(item.url))
            else:
                if is_title_empty is True:
                    self.file.logger(self.log_path, 'Empty title for {0}'.format(item.url))
                    print 'Empty title for {0}'.format(item.url)
                print 'Finished or Empty title for {0}'.format(item.url)
        print 'End to parse {0}'.format(current_url)

        del current_url, results, html
        gc.collect()

    def start(self):
        if self.doraemon.isCamelReadyToRun(self.settings) is False:
            self.file.logger(self.log_path, 'It is not ready to run for {0}'.format(self.name))
            print 'It is not ready to run for {0}'.format(self.name)
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)

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
        self.doraemon.recoveryConcurrency()
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

        del new_urls, content, url_list, request
        gc.collect()

if __name__ == '__main__':
    camelBone=CamelBone()
    camelBone.start()