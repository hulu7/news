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

class Cankaoxiaoxi():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.CANKAOXIAOXI['WORK_PATH_PRD2']
        self.mongo = Settings.CANKAOXIAOXI['MONGO_URLS']
        self.name = Settings.CANKAOXIAOXI['NAME']
        self.max_pool_size = Settings.CANKAOXIAOXI['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.CANKAOXIAOXI['URLS']
        self.restart_path = Settings.CANKAOXIAOXI['RESTART_PATH']
        self.restart_interval = Settings.CANKAOXIAOXI['RESTART_INTERVAL']
        self.today = Settings.TODAY

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            if 'html' not in href_url:
                continue
            if len(self.goodkeys) > 0:
                for good in self.goodkeys:
                    if valid == True:
                        continue
                    if good in href_url:
                        valid = True
            if len(self.badkeys) > 0:
                for bad in self.badkeys:
                    if valid == False:
                        continue
                    if bad in href_url:
                        valid = False
            if valid:
                short_url_parts = re.split(r'[., /, _, ?, #]', href_url)
                if len(short_url_parts) < 2:
                    continue
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                title = ''
                title0_1 = item.xpath(".//div/h3/text()")
                title0_2 = item.xpath(".//h3/text()")
                title0_3 = item.xpath("@title")
                if self.doraemon.isEmpty(title0_1) is False:
                    title = ''.join(title0_1)
                if self.doraemon.isEmpty(title0_2) is False:
                    title = ''.join(title0_2)
                if self.doraemon.isEmpty(title0_3) is False:
                    title = ''.join(title0_3)
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
        self.badkeys = ['mid', 'about', 'photo', 'index']
        self.goodkeys = []
        new_urls = []
        for url in  self.urls:
            new_urls.append([url, ''])
        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

if __name__ == '__main__':
    cankaoxiaoxi=Cankaoxiaoxi()
    cankaoxiaoxi.start_requests()