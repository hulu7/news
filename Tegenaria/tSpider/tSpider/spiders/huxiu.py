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
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Huxiu():

    def __init__(self):

        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(Settings.LOG_PATH)

    def getSettings(self):
        self.work_path_prd1 = Settings.HUXIU['WORK_PATH_PRD1']
        self.finished_txt_path = Settings.HUXIU['FINISHED_TXT_PATH']
        self.url_path = Settings.HUXIU['URL_PATH']
        self.mongo = Settings.HUXIU['MONGO']
        self.name = Settings.HUXIU['NAME']
        self.max_pool_size = Settings.HUXIU['MAX_POOL_SIZE']
        self.log_path = Settings.LOG_PATH
        self.today = Settings.TODAY
        self.is_open_cache = Settings.HUXIU['IS_OPEN_CACHE']

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
        title1 = html.xpath(".//*[contains(@class,'t-h1')]/text()")
        comment_number1 = html.xpath(".//*[contains(@class, 'article-pl pull-left')]/text()")
        share_number1 = html.xpath(".//*[contains(@class, 'article-share pull-left')]/text()")
        image_url1 = html.xpath(".//*[contains(@class, 'article-img-box')]/img/@src")
        content1 = html.xpath(".//div[contains(@class, 'article-content-wrap')]//*/text()")
        time1 = html.xpath(".//*[contains(@class, 'article-time')]/text()")
        author_url1 = html.xpath(".//*[contains(@class, 'author-name')]/a/@href")
        author_name1 = html.xpath(".//*[contains(@class, 'author-name')]/a/text()")

        if self.doraemon.isEmpty(title1) is False:
            title = title1[0].strip()
        if self.doraemon.isEmpty(comment_number1) is False:
            comment_number = str(filter(str.isdigit, comment_number1[0].encode('gbk'))).strip()
        if self.doraemon.isEmpty(share_number1) is False:
            share_number = str(filter(str.isdigit, share_number1[0].encode('gbk'))).strip()
        if self.doraemon.isEmpty(image_url1) is False:
            image_url = image_url1[0].strip()
        if self.doraemon.isEmpty(content1) is False:
            content = ''.join(content1).strip()
            valid = True
        if self.doraemon.isEmpty(time1) is False:
            time = time1[0]
        if self.doraemon.isEmpty(author_url1) is False:
            author_url = urlparse.urljoin(current_url, author_url1[0].strip())
        if self.doraemon.isEmpty(author_name1) is False:
            author_name = author_name1[0].strip()

        data = {
            'title': title,
            'comment_number': comment_number,
            'share_number': share_number,
            'image_url': image_url,
            'url': url,
            'time': time,
            'author_url': author_url,
            'author_name': author_name,
            'id': id,
            'download_time': self.today,
            'is_open_cache': self.is_open_cache
        }
        print 'End to parse: {0}'.format(current_url)
        if valid == True:
            self.file.logger(self.log_path, 'Start to store mongo {0}'.format(data['url']))
            print 'Start to store mongo {0}'.format(data['url'])
            self.doraemon.storeMongodb(self.mongo, data)
            self.file.logger(self.log_path, 'End to store mongo {0}'.format(data['url']))
            print 'End to store mongo {0}'.format(data['url'])
            self.doraemon.storeTxt(id, content, self.finished_txt_path, self.name)
            self.doraemon.storeFinished(response['request_title'])
        else:
            self.doraemon.storeFinished(response['request_title'])
        del current_url, html, title, comment_number, share_number, image_url, url, content, time, author_url, author_name, id, data
        gc.collect()

    def start_requests(self):
        self.file.logger(self.log_path, 'Start request: {0}'.format(self.name))
        print 'Start ' + self.name + ' requests'
        new_url_titles = self.doraemon.readNewUrls(self.url_path)
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