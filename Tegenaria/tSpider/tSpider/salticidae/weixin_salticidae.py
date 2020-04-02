# -*- coding: utf-8 -*-
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
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
        self.doraemon.createFilePath(self.finished_img_path)

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
        self.regx_img = re.compile('<img(.*?)/>')
        self.regx_date = re.compile('<em id="publish_time" class="rich_media_meta rich_media_meta_text">(.*?)</em>')
        self.regx_img_type = re.compile('data-type="(.*?)"')
        self.regx_img_data_src = re.compile('data-src="(.*?)"')
        self.regx_img_src = re.compile('src="(.*?)"')
        self.regx_img_class = re.compile('class="(.*?)"')

    def getPostFixOfImage(self, image_type):
        if image_type == 'jpeg':
            return 'jpg'
        if image_type == 'png':
            return 'png'
        if image_type == 'gif':
            return 'gif'
        else:
            print 'Other type: {0}'.format(image_type)

    def start_requests(self):
        self.file.logger(self.log_path, 'Start dowload images for: {0} '.format(self.name))
        print 'Start dowload images for: {0} '.format(self.name)
        new_ids = self.doraemon.readNewImageIds(self.doraemon.bf_finished_image_id, self.finished_content_path)
        if len(new_ids) == 0:
            self.file.logger(self.log_path, 'No new image id for {0}'.format(self.name))
            print 'No new image id for {0}'.format(self.name)
            return
        self.doraemon.createFilePath(self.finished_processed_html_path)
        self.doraemon.createFilePath(self.finished_img_path)
        for id in new_ids:
            print 'Start to remove pictures in: {0}'.format(id)
            html_file = self.file.readFromHtml("{0}/{1}.html".format(self.finished_origin_html_path, id))
            img_list = re.findall(self.regx_img, html_file)
            date_list = re.findall(self.regx_date, html_file)
            new_html = ''
            number = 0
            for old_time in date_list:
                new_date = self.doraemon.getDateFromString(old_time)
                old_time_content = '<em id="publish_time" class="rich_media_meta rich_media_meta_text">{0}</em>'.format(old_time)
                new_time_content = '<em id="publish_time" class="rich_media_meta rich_media_meta_text">{0}</em>'.format(new_date)
                new_html = html_file.replace(old_time_content, new_time_content)
                html_file = new_html
            for img in img_list:
                old_img = img
                image_id = "{0}_{1}".format(id, number)
                image_data_src = ''.join(re.findall(self.regx_img_data_src, img)).strip()
                image_src = re.findall(self.regx_img_src, img)
                image_type = ''.join(re.findall(self.regx_img_type, img)).strip()
                image_post_fix = self.getPostFixOfImage(image_type)
                if (self.doraemon.isEmpty(image_data_src) is True) or \
                   (self.doraemon.isEmpty(image_src) is True) or \
                   (self.doraemon.isEmpty(image_type) is True):
                    continue
                origin_image_path = "{0}/{1}.{2}".format(self.finished_img_path, image_id, image_post_fix)
                print 'Start to download image: {0}'.format(image_data_src)
                self.doraemon.downloadImage(image_data_src, origin_image_path)
                image_size = self.doraemon.getFileSize(origin_image_path)
                if image_size > 60:
                    print 'Start to compress image: {0}'.format(image_data_src)
                    self.doraemon.compressImage(origin_image_path, origin_image_path, 2)
                    print 'Finished to compress image: {0}'.format(image_data_src)
                print 'Finished to download image: {0}'.format(image_data_src)
                print 'Start to replace image url: {0}'.format(image_id)
                new_imgurl = "{0}{1}.{2}".format(self.url_deepinews_10002_image, image_id, image_post_fix)
                # new_imgurl = '/home/dev/Data/rsyncData/prd4/weixin/img/{0}.{1}'.format(image_id, image_post_fix)
                src_list = re.findall(self.regx_img_src, img)
                img_class_list = re.findall(self.regx_img_class, img)
                for img_class in img_class_list:
                    new_img = img.replace(img_class, 'rich_pages')
                    img = new_img
                for src in src_list:
                    new_img = img.replace(src, new_imgurl)
                    img = new_img
                new_html = html_file.replace(old_img, img)
                html_file = new_html
                print 'Finished to replace image url: {0}'.format(image_id)
                number += 1
            self.doraemon.storeHtml(id, new_html, self.finished_processed_html_path)
            self.doraemon.storeFinished(self.doraemon.bf_finished_image_id, id)

if __name__ == '__main__':
    WeixinSalticidae=WeixinSalticidae()
    WeixinSalticidae.start_requests()