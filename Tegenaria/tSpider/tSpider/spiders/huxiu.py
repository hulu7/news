#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import gc
import time
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Huxiu():

    def __init__(self):
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(self.globalSettings.LOG_PATH)
        self.time = time

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings('huxiu')
        self.log_path = self.globalSettings.LOG_PATH
        self.today = self.globalSettings.TODAY

        self.source = self.settings.SOURCE_NAME
        self.work_path_prd1 = self.settings.WORK_PATH_PRD1
        self.finished_txt_path = self.settings.FINISHED_TXT_PATH
        self.url_path = self.settings.URL_PATH
        self.mongo = self.settings.MONGO
        self.name = self.settings.NAME
        self.max_pool_size = self.settings.MAX_POOL_SIZE
        self.is_open_cache = self.settings.IS_OPEN_CACHE

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        data = {}
        comment_number = ""
        title = ""
        url = ""
        id = ""
        share_number = ""
        image_url = ""
        content = ""
        time = ""
        author_url = ""
        author_name = ""
        valid = False

        url = current_url
        id = str(filter(str.isdigit, current_url.encode('gbk')))
        title1 = html.xpath(".//*[contains(@class,'article__title')]/text()")
        content1 = html.xpath(".//*[contains(@class, 'article__content')]//*//text()")
        time1 = html.xpath(".//*[contains(@class, 'article__time')]/text()")
        author_url1 = html.xpath(".//*[contains(@class, 'author-info__username')]//text()")
        author_name1 = self.name
        images0_1 = html.xpath(".//*[contains(@class,'top-img')]//img//@src")
        images0_2 = html.xpath(".//*[contains(@class,'img-center-box')]//img//@src")
        self.time.sleep(2)
        if self.doraemon.isEmpty(title1) is False:
            title = title1[0].strip()
        if self.doraemon.isEmpty(content1) is False:
            content = ''.join(content1).strip()
            valid = True
        if self.doraemon.isEmpty(time1) is False:
            time = ''.join(time1).strip()
            time = self.doraemon.getDateFromString(time)
        if self.doraemon.isEmpty(author_url1) is False:
            author_url = author_url1[0].strip()
        if self.doraemon.isEmpty(author_name1) is False:
            author_name = author_name1

        images = []
        images0_1 = self.doraemon.completeImageUrls(images0_1, url)
        images0_2 = self.doraemon.completeImageUrls(images0_2, url)
        self.doraemon.updateImages(images, images0_1)
        self.doraemon.updateImages(images, images0_2)

        data = self.doraemon.createSpidersData(url.strip(),
                                               time.strip(),
                                               author_name.strip(),
                                               title.strip(),
                                               id.strip(),
                                               self.today,
                                               self.source,
                                               images,
                                               self.is_open_cache)

        print 'End to parse: {0}'.format(current_url)
        if valid == True:
            self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
            print 'Start to store mongo {0}'.format(data['url'])
            self.doraemon.storeMongodb(self.mongo, data)
            self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
            print 'End to store mongo {0}'.format(data['url'])
            self.doraemon.storeTxt(id, content, self.finished_txt_path, self.name)
            self.doraemon.storeFinished(self.doraemon.bf_content, response['request_title'])
        else:
            self.doraemon.storeFinished(self.doraemon.bf_content, response['request_title'])
        del current_url, html, title, comment_number, share_number, image_url, url, content, time, author_url, author_name, id, data
        gc.collect()

    def start_requests(self):
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start ' + self.name + ' requests'
        new_url_titles = self.doraemon.readNewUrls(self.doraemon.bf_content, self.url_path)
        if len(new_url_titles) == 0:
            self.file.logger(self.log_path, 'No new url for: {0}'.format(self.name))
            print 'No new url for: {0}'.format(self.name)
            return
        request = BrowserRequest()
        content = request.start_chrome(new_url_titles, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.file.logger(self.log_path, 'End requests: {0}'.format(str(len(content))))
        print 'End requests: {0}'.format(str(len(content)))
        del new_url_titles, request, content
        gc.collect()

if __name__ == '__main__':
    huxiu=Huxiu()
    huxiu.start_requests()