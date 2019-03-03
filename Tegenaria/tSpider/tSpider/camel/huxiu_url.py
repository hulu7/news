#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import urlparse
import re
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Huxiu():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.HUXIU['WORK_PATH_PRD2']
        self.mongo = Settings.HUXIU['MONGO_URLS']
        self.name = Settings.HUXIU['NAME']
        self.max_pool_size = Settings.HUXIU['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.HUXIU['URLS']
        self.restart_path = Settings.HUXIU['RESTART_PATH']
        self.restart_interval = Settings.HUXIU['RESTART_INTERVAL']
        self.today = Settings.TODAY

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//*[contains(@class,'transition msubstr-row2')]")
        for item in href_items:
            short_url = item.xpath("@href")[0]
            id = str(filter(str.isdigit, short_url.encode('gbk')))
            url = urlparse.urljoin(current_url, short_url)
            title = item.text
            is_title_empty = self.doraemon.isEmpty(title)
            if (is_title_empty is False) and (self.doraemon.isDuplicated(title) is False):
                data = {
                    'title': title.strip(),
                    'url': url.strip(),
                    'id': id.strip(),
                    'download_time': self.today
                }
                self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
                print 'Start to store mongo {0}'.format(data['url'])
                self.doraemon.storeMongodb(self.mongo, data)
                self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
                print 'End to store mongo {0}'.format(data['url'])
                self.file.logger(self.log_path, 'End to parse: {0}'.format(current_url))
            else:
                print 'Url exits: {0}'.format(url)
        print 'End to parse: {0}'.format(current_url)

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start requests: {0}'.format(self.name))
        print 'Start requests: {0}'.format(self.name)
        new_urls = []
        for url in  self.urls:
            new_urls.append([url, ''])
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

if __name__ == '__main__':
    huxiu=Huxiu()
    huxiu.start_requests()