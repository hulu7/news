#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree

sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class XueqiuReceptor():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)

    def getSettings(self):
        self.work_path_prd2 = "/home/dev/Data/rsyncData/test/"
        self.mongo = "xueqiu_content_test"
        self.finished_ids = "xueqiu_content_test"
        self.log_path = "/home/dev/Data/rsyncData/test/"

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title'].strip()
        href_contens = html.xpath("./*[contains(@class, 'date-and-source')]")
        if len(href_contens) == 0:
            print 'No data for: {0}'.format(key)
            return
        texts = href_contens[0].xpath(".//text()")
        time_source = ''.join(texts).strip()
        self.doraemon.hashSet(self.finished_ids, current_url, current_url)
        data = {
            'id': key,
            'url': current_url,
            'date': time_source
        }
        print 'Start to store mongo {0}'.format(data['url'])
        self.doraemon.storeMongodb(self.mongo, data)
        print 'Finished for {0}'.format(key)


    def start_requests(self):
        print 'Start requests'
        new_urls = []
        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_ids))
        file_path = '/home/dev/Data/rsyncData/test/xueqiu_content.csv'
        items = self.file.readFromCSV(file_path)
        items.pop(0)

        for item in items:
            key = item[0]
            if key not in all_finished_id:
                name = key.strip()
                url = item[1]
                new_urls.append([url, name])

        if len(new_urls) == 0:
            print 'No more urls.'
            return

        request = BrowserRequest()
        request.start_chrome(new_urls, 2, self.log_path, None, callback=self.parse)

if __name__ == '__main__':
    xueqiuReceptor=XueqiuReceptor()
    xueqiuReceptor.start_requests()