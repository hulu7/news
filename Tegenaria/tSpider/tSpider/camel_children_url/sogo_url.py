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
import requests
import time
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Sogo():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = Settings.SOGO['WORK_PATH_PRD2']
        self.mongo = Settings.SOGO['MONGO_URLS']
        self.name = Settings.SOGO['NAME']
        self.max_pool_size = Settings.SOGO['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH_PRD2
        self.urls = Settings.SOGO['URLS']
        self.restart_path = Settings.SOGO['RESTART_PATH']
        self.restart_interval = Settings.SOGO['RESTART_INTERVAL']
        self.proxy_pool = Settings.PROXY_POOL
        self.valid_proxy_name = Settings.VALID_PROXY_CHILDREN_URL
        self.finished_gongzhonghao_id = Settings.FINISHED_GONGZHONGHAO_ID
        self.invalid_proxy_name = Settings.INVALID_PROXY_CHILDREN_URL
        self.finished_gongzhonghao_aritcle_list_id = Settings.FINISHED_GONGZHONGHAO_ARTICLE_LIST_ID
        self.today = Settings.TODAY
        self.url_pool = Settings.SETTINGS_GONGZHONGHAO

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'weui_media_bd')]")
        if len(href_item) == 0:
            self.doraemon.hashSet(self.invalid_proxy_name, self.proxy, self.proxy)
            self.doraemon.delHashSet(self.valid_proxy_name, self.proxy)
            all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_name))
            self.proxy = all_valid_proxy.pop()
            print 'Blocked for {0} -- id: {1}'.format(key, self.proxy)
            self.file.logger(self.log_path, 'Blocked for {0} -- id: {1}'.format(key, self.proxy))
            return

        for item in href_item:
            href = item.xpath(".//*[contains(@class, 'weui_media_title')]/@hrefs")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
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
                id = self.current_url[0][1]
                url = urlparse.urljoin(current_url, href_url)
                copyright = item.xpath(".//*[contains(@class, 'icon_original_tag')]")
                if len(copyright) > 0:
                    title = item.xpath(".//*[contains(@class, 'weui_media_title')]/span")[0].tail
                else:
                    title = item.xpath(".//*[contains(@class, 'weui_media_title')]")[0].text
                is_title_empty = title == None or self.doraemon.isEmpty(title)
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

        self.doraemon.hashSet(self.finished_gongzhonghao_aritcle_list_id, id, id)
        self.current_url.pop()
        print 'Finished for {0} -- id: {1}'.format(id, self.proxy)
        self.file.logger(self.log_path, 'Finished for {0} -- id: {1}'.format(id, self.proxy))
        if len(self.new_urls) > 0:
            new_url = self.new_urls.pop()
            print 'Start next: {0}'.format(new_url[0])
            self.current_url.append(new_url)
        print 'End to parse {0}, url: {1}'.format(id, href_item[0])

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)
        self.new_urls = []
        self.current_url = []
        response = requests.get(self.proxy_pool)
        proxy_pool = eval(response.content)
        all_invalid_proxy = list(self.doraemon.getAllHasSet(self.invalid_proxy_name))
        for proxy in proxy_pool:
            ip_port = '{0}:{1}'.format(proxy[0], proxy[1])
            # valid_proxy.append(ip_port)
            if ip_port not in all_invalid_proxy:
                self.doraemon.hashSet(self.valid_proxy_name, ip_port, ip_port)
        all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_name))
        self.proxy = all_valid_proxy.pop()
        finished_gongzhonghao_aritcle_list_id = list(self.doraemon.getAllHasSet(self.finished_gongzhonghao_aritcle_list_id))

        self.urls_article_list = self.doraemon.getAllHasSet(self.url_pool)
        for key in self.urls:
            url = self.urls_article_list[key]
            if key not in finished_gongzhonghao_aritcle_list_id:
                self.new_urls.append([url, key])

        if len(self.new_urls) > 0:
            self.current_url.append(self.new_urls.pop())
        else:
            print 'No more urls.'
            return
        self.badkeys = ['None']
        self.goodkeys = ['']
        request = BrowserRequest()
        while len(self.current_url) > 0:
            request.start_chrome(self.current_url, self.max_pool_size, self.log_path, self.proxy, callback=self.parse)
        self.file.logger(self.log_path, 'End for requests of {0}.'.format(self.name))

if __name__ == '__main__':
    Sogo=Sogo()
    Sogo.start_requests()