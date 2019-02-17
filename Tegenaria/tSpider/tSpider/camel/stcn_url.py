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

class Stcn():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.STCN['WORK_PATH_PRD2']
        self.mongo = Settings.STCN['MONGO_URLS']
        self.name = Settings.STCN['NAME']
        self.max_pool_size = Settings.STCN['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.STCN['URLS']
        self.restart_path = Settings.STCN['RESTART_PATH']
        self.restart_interval = Settings.STCN['RESTART_INTERVAL']

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")
        keys = ['certificate', 'pdf', 'video', 'filepublish']
        for item in href_items:
            href = item.xpath("@href")
            hasKeys = False
            if len(href) == 0:
                continue
            if len(str(filter(str.isdigit, href[0]))) == 0:
                continue
            if 'html' not in href[0]:
                continue
            for key in keys:
                if key in href[0]:
                    hasKeys = True
            if hasKeys == True:
                continue
            short_url = href[0]
            short_url_parts = re.split(r'[., /, _]', short_url)
            id = short_url_parts[len(short_url_parts) - 2]
            url = urlparse.urljoin(current_url, short_url)
            title = item.xpath("@title")
            if len(title) == 0:
                continue
            title = title[0]
            is_title_empty = self.doraemon.isEmpty(title)
            if (is_title_empty is False) and (self.doraemon.isDuplicated(title) is False):
                data = {
                    'title': title.strip(),
                    'url': url.strip(),
                    'id': id.strip()
                }
                self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
                print 'Start to store mongo {0}'.format(data['url'])
                self.doraemon.storeMongodb(self.mongo, data)
                self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
                print 'End to store mongo {0}'.format(data['url'])
                self.file.logger(self.log_path, 'End to parse: {0}'.format(current_url))
            else:
                print 'Empty title for: {0}'.format(url)

        print 'End to parse: {0}'.format(current_url)

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        new_urls = self.urls
        # new_urls = ['http://www.stcn.com/']
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

if __name__ == '__main__':
    stcn=Stcn()
    stcn.start_requests()