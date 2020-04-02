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

sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class WoshipmReceptor():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)

    def getSettings(self):
        self.work_path_prd2 = "/home/dev/Data/rsyncData/test/"
        self.mongo = "whoispm_receptor"
        self.finished_ids = "woshipm_receptor"
        self.log_path = "/home/dev/Data/rsyncData/test/"
        self.regx = re.compile("/u/[0-9]{0,}")

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title'].strip()
        href_contens = html.xpath("./a")
        if len(href_contens) == 0:
            print 'No data for: {0}'.format(key)
            return
        for item in href_contens:
            href = item.xpath("@href")
            title_content = item.xpath(".//text()")
            title = "".join(title_content).strip()
            if len(href) > 0 and title == key:
                isValidUrl = self.regx.match(href[0])
                if isValidUrl is None:
                    print 'Invalid url for not match: {0}'.format(href[0])
                    continue
                url = "http://www.woshipm.com{0}".format(href[0])
                self.doraemon.hashSet(self.finished_ids, url, url)
                data = {
                    'id': key,
                    'url': url
                }
                print 'Start to store mongo {0}'.format(data['url'])
                self.doraemon.storeMongodb(self.mongo, data)
                print 'Finished for {0}'.format(key)

    def start_requests(self):
        print 'Start requests'
        new_urls = []
        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_ids))
        txt_path = '/home/dev/Data/rsyncData/test/woshipm_receptor.txt'
        gonzhonghao = self.file.readFromTxt(txt_path)
        keys = gonzhonghao.split('\n')

        for key in keys:
            key = key.strip()
            if key not in all_finished_id:
                name = key.strip()
                tmp_url = "http://www.woshipm.com/search-posts?k={0}".format(name)
                new_urls.append([tmp_url, name])
            else:
                print 'Finished or no data for {0}'.format(key)
                self.doraemon.hashSet(self.finished_ids, key, key)

        if len(new_urls) == 0:
            print 'No more urls.'
            return

        request = BrowserRequest()
        request.start_chrome(new_urls, 2, self.log_path, None, callback=self.parse)

if __name__ == '__main__':
    woshipm=WoshipmReceptor()
    woshipm.start_requests()