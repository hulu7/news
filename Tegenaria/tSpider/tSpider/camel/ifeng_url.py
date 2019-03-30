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

class Ifeng():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('ifeng')
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
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//a")

        for item in href_items:
            href = item.xpath("@href")
            if len(href) == 0:
                continue

            href_url = href[0]

            if self.name not in href_url:
                continue

            if '/c/' not in href_url:
                if 'html' not in href_url:
                    continue

            title0_1 = ''.join(item.xpath(".//*[contains(@class,'i_con_l')]/h3/text()")).strip()
            title0_2 = item.xpath(".//text()")
            title0_3 = ''.join(item.xpath(".//*[contains(@class,'i-title')]/text()")).strip()
            title = ''

            if len(title0_1) > 0:
                title = title0_1
            elif len(title0_2) == 1:
                title = title0_2[0].strip()
            elif len(title0_3) > 0:
                title = title0_3
            if len(title) == 0 or str.isdigit(str(title)):
                continue

            valid = False
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

            if valid == True:
                short_url = href_url.strip()
                url = urlparse.urljoin(current_url, short_url.strip())

                short_url_parts = re.split(r'[., /, _]', url)
                if '/c/' in short_url:
                    id_index = short_url_parts.index('c') + 1
                    id = short_url_parts[id_index]
                elif 'news' in short_url:
                    id_index = short_url_parts.index('ifeng') + 2
                    id = short_url_parts[id_index].strip()
                else:
                    continue

                if self.doraemon.isEmpty(id):
                    continue

                if self.doraemon.isDuplicated(title) is False:
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
                    self.file.logger(self.log_path, 'End to parse: {0}'.format(current_url))
                else:
                    print 'Url exits: {0}'.format(url)
        print 'End to parse: {0}'.format(current_url)

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start request: {0}'.format(self.name)
        self.goodkeys = ['ifeng', 'news']
        self.badkeys = ['jpg', 'yc', '#p', 'cosmetics', 'weidian', 'homedetail', 'detail?', 'weather', 'idyn',
                        'quanmeiti', 'srctag', 'market', 'tv', 'ispecial', 'icommon', 'channel', 'taiwan']
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
        # new_urls = [['https://ipit.ifeng.com/', 'TEST']]
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

if __name__ == '__main__':
    ifeng=Ifeng()
    ifeng.start_requests()