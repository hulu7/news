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

class Gongzhonghao():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd2 = settings_name['WORK_PATH_PRD2']
        self.mongo = "gongzhonghao_test"
        self.log_path = Settings.LOG_PATH_PRD2
        self.finished_ids = "gongzhonghao_test"
        self.log_path = Settings.LOG_PATH

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@class, 'pagedlist_item')]")
        if len(href_item) == 0:
            print 'No data for: {0}'.format(key)
            return
        self.doraemon.hashSet(self.finished_ids, key, key)
        data = {
            'id': key,
            'url': current_url
        }
        print 'Start to store mongo {0}'.format(data['url'])
        self.doraemon.storeMongodb(self.mongo, data)
        print 'Finished for {0}'.format(key)

    def start_requests(self):
        print 'Start requests'
        new_urls = []
        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_ids))
        txt_path = '/home/dev/Repository/news/Tegenaria/tSpider/tSpider/food/gongzhonghao_test.txt'
        gonzhonghao = self.file.readFromTxt(txt_path)
        keys = gonzhonghao.split('\n')

        for key in keys:
            if key not in all_finished_id:
                tmp_url = "https://www.iivv.com/account/{0}".format(key)
                new_urls.append([tmp_url, key])

        if len(new_urls) == 0:
            print 'No more urls.'
            return

        request = BrowserRequest()
        request.start_chrome(new_urls, 2, self.log_path, None, callback=self.parse)

if __name__ == '__main__':
    Gongzhonghao=Gongzhonghao()
    Gongzhonghao.start_requests()