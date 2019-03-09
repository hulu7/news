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

class Yicai():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.YICAI['WORK_PATH_PRD2']
        self.mongo = Settings.YICAI['MONGO_URLS']
        self.name = Settings.YICAI['NAME']
        self.max_pool_size = Settings.YICAI['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.YICAI['URLS']
        self.restart_path = Settings.YICAI['RESTART_PATH']
        self.restart_interval = Settings.YICAI['RESTART_INTERVAL']
        self.today = Settings.TODAY

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")
        if len(href_items) == 0:
            return
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            if 'html' not in href_url:
                continue
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
                title_content0_1 = item.xpath(".//div/h2/text()")
                title_content0_2 = item.xpath(".//div/h3/span/text()")
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                if len(title_content0_1) != 0:
                    title = title_content0_1[0]
                elif len(title_content0_2) != 0:
                    title = title_content0_2[0]
                else:
                    title = ""
                is_valid_id = len(str(filter(str.isdigit, id))) != 0
                is_title_empty = title == None or self.doraemon.isEmpty(title)
                if (is_valid_id is True) and (is_title_empty is False) and (self.doraemon.isDuplicated(title) is False):
                    data = {
                        'title': title,
                        'url': url,
                        'id': id,
                        'download_time': self.today
                    }
                    self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
                    print 'Start to store mongo {0}'.format(data['url'])
                    self.doraemon.storeMongodb(self.mongo, data)
                    self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
                    print 'End to store mongo {0}'.format(data['url'])
                    self.file.logger(self.log_path, 'End to parse: {0}'.format(current_url))
                else:
                    print 'Url exits or empty: {0}'.format(url)
                    if is_title_empty is True:
                        self.file.logger(self.log_path, 'Empty title for: {0}'.format(url))
                        print 'Empty title for {0}'.format(url)
        print 'End to parse: {0}'.format(current_url)

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        self.badkeys = ['daohang', 'video']
        self.goodkeys = ['']

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
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

if __name__ == '__main__':
    yicai=Yicai()
    yicai.start_requests()