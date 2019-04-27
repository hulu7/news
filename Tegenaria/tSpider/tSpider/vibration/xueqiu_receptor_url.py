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
        self.work_path_prd2 = "//home//dev//Data//rsyncData//test//"
        self.mongo = "xueqiu_test"
        self.finished_ids = "xueqiu_test"
        self.log_path = "//home//dev//Data//rsyncData//test//"

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title'].strip()
        href_contens = html.xpath(".//*[contains(@class, 'search__user__card__content')]")
        if len(href_contens) == 0:
            print 'No data for: {0}'.format(key)
            return
        for item in href_contens:
            href = item.xpath(".//*[contains(@class, 'user-name')]/@href")
            title_content = item.xpath(".//*[contains(@class, 'user-name')]//span/text()")
            title = "".join(title_content).strip()
            if len(href) > 0 and title == key:
                url = "https://xueqiu.com/u{0}".format(href[0])
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
        txt_path = '/home/dev/Data/rsyncData/test/xueqiu.txt'
        gonzhonghao = self.file.readFromTxt(txt_path)
        keys = gonzhonghao.split('\n')

        for key in keys:
            if key not in all_finished_id:
                name = key.strip()
                tmp_url = "https://xueqiu.com/k?q={0}".format(name)
                new_urls.append([tmp_url, name])

        if len(new_urls) == 0:
            print 'No more urls.'
            return

        request = BrowserRequest()
        request.start_chrome(new_urls, 5, self.log_path, None, callback=self.parse)

if __name__ == '__main__':
    xueqiuReceptor=XueqiuReceptor()
    xueqiuReceptor.start_requests()