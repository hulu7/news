#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import re
import datetime
import urlparse
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest_weixin import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon
from middlewares.requestsMiddleware import RequestsMiddleware

class Weixin():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.request = RequestsMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.log_path)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('weixin')
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
        self.regx = re.compile("/s\?timestamp=[0-9]{0,}&src=[0-9]{0,}&ver=[0-9]{0,}&signature=(.*?)")

    def parse(self, response):
        if len(response['response']) == 0:
            print 'ip is blocked'
            return
        current_url = response['response'].current_url.encode('gbk')
        weixinId = response['request_title'].encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        href_items = html.xpath(".//*[contains(@class,'weui_media_bd')]")
        for item in href_items:
            href = item.xpath(".//*[contains(@class,'weui_media_title')]/@hrefs")
            if len(href) == 0:
                print 'Url is empty'
                return
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            isValidUrl = self.regx.match(href_url)
            if isValidUrl is None:
                print 'Invalid url for not match: {0}'.format(href_url)
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
                short_url_parts = re.split(r'signature=', href_url)
                id = ''.join(short_url_parts[1]).strip()
                p_time = item.xpath(".//*[contains(@class,'weui_media_extra_info')]/text()")
                url = urlparse.urljoin(current_url, href_url)
                is_p_time_missing = False
                if self.doraemon.isEmpty(str(p_time)):
                    is_p_time_missing = True
                    self.file.logger(self.log_path, 'publish time missing for {0}'.format(current_url))
                    p_time = int(short_url_parts[short_url_parts.index('timestamp') + 1])
                    p_time = datetime.datetime.fromtimestamp(p_time).strftime("%Y-%m-%d")
                p_time = ''.join(p_time).strip()
                publish_time = self.doraemon.getDateFromString(p_time)
                title = item.xpath(".//*[contains(@class,'weui_media_title')]/text()")
                title = ''.join(title).strip()
                is_title_empty = self.doraemon.isEmpty(title)
                if (is_title_empty is False) and (self.doraemon.isDuplicated(self.doraemon.bf_weixin_url, title) is False):
                    if self.doraemon.isFinished(self.doraemon.bf_weixin_id, weixinId) is False and is_p_time_missing is False and publish_time == self.today:
                        self.doraemon.storeFinished(self.doraemon.bf_weixin_id, weixinId)
                    data = {
                        'title': title,
                        'url': url,
                        'id': id,
                        'download_time': self.today,
                        'publish_time': publish_time,
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
                self.file.logger(self.log_path, 'Invalid {0}'.format(current_url))
                print 'Invalid {0}'.format(current_url)
        print 'End to parse {0}'.format(current_url)

        del current_url, html, title, url, id, data, short_url_parts
        gc.collect()

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.badkeys = []
        self.goodkeys = []
        new_urls = []
        content = self.file.readFromTxt(self.urls)
        id_list = content.strip().split('\n')

        for id in id_list:
            if self.doraemon.isEmpty(id) is False and self.doraemon.isFinished(self.doraemon.bf_weixin_id, id) is False:
                new_urls.append([id, id])

        if len(new_urls) == 0:
            print 'No url.'
            return
        self.file.logger(self.log_path, 'There is {0} weixin requests to do.'.format(str(len(new_urls))))

        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, '121.234.244.59:30101', callback=self.parse)
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

        del new_urls, content, id_list, request
        gc.collect()

if __name__ == '__main__':
    Weixin=Weixin()
    Weixin.start_requests()