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
import json
import gc
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon
from Tegenaria.tSpider.tSpider.middlewares.requestsMiddleware import RequestsMiddleware

class Camel():

    def __init__(self):
        self.request = RequestsMiddleware()
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.globalSettings.LOG_PATH)

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings('weixin')
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
        weixinId = response['request_title'].encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        json_content_list = html.xpath(".//pre/text()")
        if len(json_content_list) == 0:
            print 'There is no data for weixin: {0}'.format(weixinId)
            self.file.logger(self.log_path, 'There is no data for weixin: {0}'.format(weixinId))
            return
        content = json.loads(json_content_list[0])
        if content['error_code'] != 0:
            print 'No content for weixin id: {0}'.format(weixinId)
            self.file.logger(self.log_path, 'No content for weixin id: {0}'.format(weixinId))
            return
        items = content['data']['articles']
        if len(items) == 0:
            print 'No url for weixin id: {0}'.format(weixinId)
            self.file.logger(self.log_path, 'No url for weixin id: {0}'.format(weixinId))
            return
        for item in items:
            url = item['article_url']
            valid = True
            if len(url) == 0:
                print 'Invalid url for weixin id: {0}'.format(weixinId)
                continue
            for good in self.goodkeys:
                if valid == True:
                    continue
                if good in url:
                    valid = True
            for bad in self.badkeys:
                if valid == False:
                    continue
                if bad in url:
                    valid = False
            if valid:
                if 'signature' not in url:
                    print "No signature in url {0}".format(url)
                    continue
                short_url_parts = re.split(r'[., /, _, %, ", -, =, ?]', url)
                id = ''.join(short_url_parts[short_url_parts.index('signature') + 1:]).strip()
                p_time = item['article_publish_time']
                is_p_time_missing = False
                if self.doraemon.isEmpty(str(p_time)):
                    is_p_time_missing = True
                    self.file.logger(self.log_path, 'publish time missing for {0}'.format(current_url))
                    p_time = int(short_url_parts[short_url_parts.index('timestamp') + 1])
                publish_time = datetime.datetime.fromtimestamp(p_time).strftime("%Y-%m-%d")
                title = item['article_title'].strip()
                is_title_empty = self.doraemon.isEmpty(title)
                if (is_title_empty is False) and (self.doraemon.isDuplicated(self.doraemon.bf_weixin_url, title) is False):
                    if self.doraemon.isFinished(self.doraemon.bf_weixin_id, weixinId) is False and is_p_time_missing is False and publish_time == self.today:
                        self.doraemon.storeFinished(self.doraemon.bf_weixin_id, weixinId)
                    data = self.doraemon.createCamelData(title.strip(),
                                                         url.strip(),
                                                         id.strip(),
                                                         self.today,
                                                         self.source)
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

        del current_url, html, title, url, id, short_url_parts
        gc.collect()

    def start_requests(self):
        return
        if self.doraemon.isCamelReadyToRun(self.settings) is False:
            self.file.logger(self.log_path, 'It is not ready to run for {0}'.format(self.name))
            print 'It is not ready to run for {0}'.format(self.name)
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.badkeys = []
        self.goodkeys = []
        appid = "137dddef7b95cffaee7e3cf870295b2b"
        new_urls = []
        content = self.file.readFromTxt(self.urls)
        id_list = content.strip().split('\n')

        for id in id_list:
            if self.doraemon.isEmpty(id) is False and self.doraemon.isFinished(self.doraemon.bf_weixin_id, id) is False:
                url = "https://api.shenjian.io/?appid={0}&weixinId={1}".format(appid, id)
                new_urls.append([url, id])

        if len(new_urls) == 0:
            print 'No url.'
            return
        self.file.logger(self.log_path, 'There is {0} weixin requests to do.'.format(str(len(new_urls))))

        request = BrowserRequest()
        content = request.start_chrome(new_urls, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.doraemon.recoveryConcurrency()
        self.file.logger(self.log_path, 'End for {0} requests of {1}.'.format(str(len(content)), self.name))
        print 'End for {0} requests of {1}.'.format(str(len(content)), self.name)

        del new_urls, content, id_list, request
        gc.collect()

if __name__ == '__main__':
    camel = Camel()
    camel.start_requests()