#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
from lxml import etree
import gc
import time
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class SpiderBone():
    def __init__(self, siteinfo=None, callback=callable):
        self.siteinfo = siteinfo
        self.callBack = callback
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(self.log_path)
        self.doraemon.createFilePath(self.finished_backup_folder_path)

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings(self.siteinfo)
        self.log_path = self.globalSettings.LOG_PATH
        self.today = self.globalSettings.TODAY
        self.source = self.settings.SOURCE_NAME
        self.work_path_prd1 = self.settings.WORK_PATH_PRD1
        self.finished_txt_path = self.settings.FINISHED_TXT_PATH
        self.finished_html_path = self.settings.FINISHED_HTML_PATH
        self.finished_image_path = self.settings.FINISHED_IMG_PATH
        self.template_path = self.globalSettings.TEMPLATE_PATH
        self.article_url = self.globalSettings.ARTICLE_URL
        self.ali_domain = self.globalSettings.ALI_DOMAIN
        self.ali_domain_deepinews = self.globalSettings.ALI_BUCKET_NAME_DEEPINEWS
        self.ali_domain_deepinews_img = self.globalSettings.ALI_BUCKET_NAME_DEEPINEWS_IMG
        self.ip_webserver0 = self.globalSettings.IP_WEBSERVER0
        self.port_webserver0 = self.globalSettings.PORT_WEBSERVER0
        self.user_root_webserver0 = self.globalSettings.USER_ROOT_WEBSERVER0
        self.user_root_password_webserver0 = self.globalSettings.USER_ROOT_PASSWORD_WEBSERVER0
        self.html_webserver0 = self.globalSettings.HTML_WEBSERVER0
        self.mongo = self.settings.MONGO
        self.name = self.settings.NAME
        self.max_pool_size = self.settings.MAX_POOL_SIZE_CONTENT
        self.url_path = self.settings.URL_PATH
        self.is_open_cache = self.settings.IS_OPEN_CACHE
        self.finished_backup_folder_path = self.settings.FINISHED_BACKUP_FOLDER_PATH
        self.max_concurrency_spider = self.globalSettings.MAX_CONCURRENCY_SPIDER
        self.concurrency_file_spider = self.globalSettings.CONCURRENCY_FILE_SPIDER

    def parse(self, response):
        time.sleep(1)
        current_url = response['response'].current_url.encode('gbk')
        request_title = response['request_title']
        print 'Start to parse: {0}'.format(current_url)
        page_source = response['response'].page_source
        html = etree.HTML(page_source)
        results = None
        try:
            results = self.callBack(current_url, html, page_source)
            if results == None:
                message1 = 'No content for: {0}'.format(current_url)
                print message1
                self.file.logger(self.log_path, message1)
                return
            dataToMongo = self.doraemon.createSpiderMongoJson(results)
        except Exception as e:
            message1 = 'Exception when parse: {0} for {1}'.format(current_url, e.message)
            print message1
            self.file.logger(self.log_path, message1)
        print 'End to parse: {0}'.format(current_url)
        if results == None:
            self.doraemon.storeFinished(self.doraemon.bf_content, request_title)
            print 'No data for {0}'.format(request_title)
        else:
            message2 = 'Start to store mongo {0}'.format(results.url)
            self.file.logger(self.log_path, message2)
            print message2
            self.doraemon.storeMongodb(self.mongo, dataToMongo)
            message3 = 'End to store mongo {0}'.format(results.url)
            self.file.logger(self.log_path, message3)
            print message3
            self.doraemon.storeTxt(results.id, results.content, self.finished_txt_path, self.name)
            self.doraemon.storeFinished(self.doraemon.bf_content, request_title)

    def start(self):
        if self.doraemon.isSpiderReadyToRun() is False:
            message4 = 'It is not ready to run spider: {0}'.format(self.name)
            print message4
            return
        message5 = 'Start {0} requests'.format(self.name)
        self.file.logger(self.log_path, message5)
        print message5
        message6 = 'Start requests: {0} '.format(self.name)
        self.file.logger(self.log_path, message6)
        print message6
        new_url_titles = self.doraemon.readNewUrls(self.doraemon.bf_content, self.url_path)
        if len(new_url_titles) == 0:
            self.doraemon.recoveryConcurrency(self.concurrency_file_spider, self.max_concurrency_spider)
            message7 = 'No new url for {0}'.format(self.name)
            self.file.logger(self.log_path, message7)
            print message7
            return
        request = BrowserRequest()
        content = request.start_chrome(new_url_titles, self.max_pool_size, self.log_path, None, callback=self.parse)
        self.doraemon.recoveryConcurrency(self.concurrency_file_spider, self.max_concurrency_spider)
        message8 = 'End requests for {0}'.format(str(len(content)))
        self.file.logger(self.log_path, message8)
        print message8
        del content, new_url_titles, request
        gc.collect()

if __name__ == '__main__':
    spiderBone=SpiderBone()
    spiderBone.start()