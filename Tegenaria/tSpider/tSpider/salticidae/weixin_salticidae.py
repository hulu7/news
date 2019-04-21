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
        self.log_path = self.settings.LOG_PATH
        self.today = self.settings.TODAY
        self.restart_path = settings_name['RESTART_PATH']
        self.restart_interval = settings_name['RESTART_INTERVAL']
        self.regx_img = re.compile('<img(.*?)/>')
        self.regx_date = re.compile('<em id="publish_time" class="rich_media_meta rich_media_meta_text">(.*?)</em>')

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
        for id in new_ids:
            print 'Start to remove pictures in: {0}'.format(id)
            html_file = self.file.readFromHtml("{0}//{1}.html".format(self.finished_origin_html_path, id))
            img_list = re.findall(self.regx_img, html_file)
            date_list = re.findall(self.regx_date, html_file)
            new_html = ''
            for old_time in date_list:
                new_date = self.doraemon.getDateFromString(old_time)
                old_time_content = '<em id="publish_time" class="rich_media_meta rich_media_meta_text">{0}</em>'.format(old_time)
                new_time_content = '<em id="publish_time" class="rich_media_meta rich_media_meta_text">{0}</em>'.format(new_date)
                new_html = html_file.replace(old_time_content, new_time_content)
                html_file = new_html
            for img in img_list:
                img_content = "{0}".format(img)
                new_html = html_file.replace(img_content, "")
                html_file = new_html
            self.doraemon.storeHtml(id, new_html, self.finished_processed_html_path)
            self.doraemon.storeFinished(self.doraemon.bf_finished_image_id, id)

if __name__ == '__main__':
    WeixinSalticidae=WeixinSalticidae()
    WeixinSalticidae.start_requests()