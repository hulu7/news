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
import json
import urllib2
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Gelonghui():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('gelonghui')
        self.source = settings_name['SOURCE_NAME']
        self.work_path_prd2 = settings_name['WORK_PATH_PRD2']
        self.mongo = settings_name['MONGO_URLS']
        self.name = settings_name['NAME']
        self.max_pool_size = settings_name['MAX_POOL_SIZE']
        self.log_path = self.settings.LOG_PATH_PRD2
        self.urls = settings_name['URLS']
        self.restart_path = settings_name['RESTART_PATH']
        self.restart_interval = settings_name['RESTART_INTERVAL']
        self.today = self.settings.TODAY

    def parse(self, response):
        current_url = response.url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        hjson = json.loads(response.read())
        data = hjson['result']

        if len(data) == 0:
            return

        for item in data:
            href_url = "https://www.gelonghui.com/p/{0}".format(item['postId'])
            hasId = str(filter(str.isdigit, href_url))
            if len(hasId) == 0:
                print 'Invalid url for no id: {0}'.format(href_url)
                continue
            valid = True
            for good in self.goodkeys:
                if valid == True:
                    continue
                if good in href_url:
                    valid = True
            for bad in self.badkeys:
                if valid == False:
                    continue
                if bad in href_url:
                    valid = False
            if valid:
                id = str(item['postId'])
                url = href_url
                title = str(item['articleTitle'])
                is_title_empty = self.doraemon.isEmpty(title)
                if (is_title_empty is False) and (self.doraemon.isDuplicated(title) is False):
                    data = {
                        'title': title.strip(),
                        'url': url.strip(),
                        'id': id.strip(),
                        'download_time': self.today,
                        'source': self.source
                    }
                    self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
                    print 'Start to store mongo {0}'.format(data['url'])
                    self.doraemon.storeMongodb(self.mongo, data)
                    self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
                    print 'End to store mongo {0}'.format(data['url'])
                    self.file.logger(self.log_path, 'Done for {0}'.format(url))
                else:
                    if is_title_empty is True:
                        self.file.logger(self.log_path, 'Empty title for {0}'.format(url))
                        print 'Empty title for {0}'.format(url)
                    print 'Finished or Empty title for {0}'.format(url)
            else:
                self.file.logger(self.log_path, 'Invalid {0}'.format(href_url))
                print 'Invalid {0}'.format(href_url)
        print 'End to parse {0}'.format(href_url)

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.badkeys = []
        self.goodkeys = []

        new_urls = []
        content = self.file.readFromTxt(self.urls)
        url_content = content.split('\n')

        for url in url_content:
            if self.doraemon.isEmpty(url) is False:
                new_urls.append(url)

        if len(new_urls) == 0:
            print 'No url.'
            return

        for url in new_urls:
            response = urllib2.urlopen(url)
            if response.code != 200:
                print 'status: ' + response.status_code
                continue
            self.parse(response)

        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(new_urls)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(new_urls)), self.name)

if __name__ == '__main__':
    gelonghui=Gelonghui()
    gelonghui.start_requests()