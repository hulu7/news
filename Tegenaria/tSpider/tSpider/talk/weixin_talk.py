# -*- coding: utf-8 -*-
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon
from middlewares.fileTransferMiddleware import FileTransferMiddleware

class WeixinTalk():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.transer = FileTransferMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('weixin')
        self.name = settings_name['NAME']
        self.log_path = self.settings.LOG_PATH
        self.host_name = self.settings.HOST_NAME
        self.user_name = self.settings.USER_NAME
        self.password = self.settings.PASSWORD
        self.port = self.settings.PORT
        self.remote_img_path = self.settings.REMOTE_IMG_PATH
        self.remote_html_path = self.settings.REMOTE_HTML_PATH
        self.max_upload_process = self.settings.MAX_UPLOAD_PROCESS
        self.temp_html_path = self.settings.TEMP_FOLDER_HTML
        self.temp_img_path = self.settings.TEMP_FOLDER_IMG

    def start_upload(self):
        html_files = self.doraemon.getFileList(self.temp_html_path)
        if len(html_files) > 0:
            if len(html_files) < 10:
                html_upload_process = 1
            else:
                html_upload_process = len(html_files) / 10
            print 'The process number for html is {0}'.format(html_upload_process)
            if html_upload_process > self.max_upload_process:
                html_upload_process = self.max_upload_process
            self.file.logger(self.log_path, 'Start upload html for: {0} '.format(self.name))
            print 'Start upload html for: {0} '.format(self.name)
            self.transer.startUpload(self.temp_html_path, self.remote_html_path, html_upload_process, self.host_name, self.user_name, self.password, self.port)
            self.file.logger(self.log_path, 'Finished upload html for: {0} '.format(self.name))
            print 'Finished upload html for: {0} '.format(self.name)
        else:
            print 'No html to upload'

        image_files = self.doraemon.getFileList(self.temp_img_path)
        if len(image_files) > 0:
            if len(image_files) < 20:
                image_upload_process = 1
            else:
                image_upload_process = len(image_files) / 20
            print 'The process number for image is {0}'.format(image_upload_process)
            if image_upload_process > self.max_upload_process:
                image_upload_process = self.max_upload_process
            self.file.logger(self.log_path, 'Start upload image for: {0} '.format(self.name))
            print 'Start upload image for: {0} '.format(self.name)
            self.transer.startUpload(self.temp_img_path, self.remote_img_path, image_upload_process, self.host_name,
                                     self.user_name, self.password, self.port)
            self.file.logger(self.log_path, 'Finished upload image for: {0} '.format(self.name))
            print 'Finished upload image for: {0} '.format(self.name)
        else:
            print 'No image to upload'

if __name__ == '__main__':
    WeixinTalk=WeixinTalk()
    WeixinTalk.start_upload()