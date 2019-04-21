# -*- coding: utf-8 -*-
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import re
import gc
from bs4 import BeautifulSoup
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class WeixinSalticidae():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd1)
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('weixin')
        self.source = settings_name['SOURCE_NAME']
        self.work_path_prd1 = settings_name['WORK_PATH_PRD1']
        self.finished_img_path = settings_name['FINISHED_IMG_PATH']
        self.finished_origin_html_path = settings_name['FINISHED_ORIGIN_HTML_PATH']
        self.finished_processed_html_path = settings_name['FINISHED_PROCESSED_HTML_PATH']
        self.finished_content_path = settings_name['FINISHED_CONTENT_PATH']
        self.mongo = settings_name['MONGO']
        self.name = settings_name['NAME']
        self.max_pool_size = settings_name['MAX_POOL_SIZE']
        self.url_deepinews_10002_article = self.settings.URL_DEEPINEWS_10002_ARTICLE
        self.url_deepinews_10002_image = self.settings.URL_DEEPINEWS_10002_IMAGE
        self.log_path = self.settings.LOG_PATH
        self.today = self.settings.TODAY
        self.restart_path = settings_name['RESTART_PATH']
        self.restart_interval = settings_name['RESTART_INTERVAL']
        self.regx = re.compile('data-src="(.+?\=jpeg)"')

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval * 0.1) is False:
            return
        self.file.logger(self.log_path, 'Start dowload images for: {0} '.format(self.name))
        print 'Start dowload images for: {0} '.format(self.name)
        new_ids = self.doraemon.readNewImageIds(self.doraemon.bf_finished_image_id, self.finished_content_path)
        if len(new_ids) == 0:
            self.file.logger(self.log_path, 'No new image id for {0}'.format(self.name))
            print 'No new image id for {0}'.format(self.name)
            return
        self.doraemon.createFilePath(self.finished_processed_html_path)
        self.doraemon.createFilePath(self.finished_img_path)
        for item in new_ids:
            id = item[0]
            html_file = self.file.readFromHtml("{0}//{1}.html".format(self.finished_origin_html_path, id))
            img_list = re.findall(self.regx, html_file)
            number = 0
            new_html = ''
            for imgurl in img_list:
                image_id = "{0}_{1}".format(id, number)
                store_url_path = "{0}//{1}.jpg".format(self.finished_img_path, image_id)
                self.doraemon.downloadImage(imgurl, store_url_path)
                print 'Finished to download image: {0}'.format(imgurl)
                new_imgurl = "{0}{1}.jpg".format(self.url_deepinews_10002_image, image_id)
                new_html = html_file.replace(imgurl, new_imgurl)
                number += 1
            self.doraemon.storeHtml(id, new_html, self.finished_processed_html_path)

if __name__ == '__main__':
    WeixinSalticidae=WeixinSalticidae()
    WeixinSalticidae.start_requests()