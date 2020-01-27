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
        try:
            self.file.logger(self.log_path, 'Start to compress html and img')
            print 'Start to compress html and img'
            self.doraemon.tar(self.temp_html_path)
            self.doraemon.tar(self.temp_img_path)
            self.file.logger(self.log_path, 'Finish to compress html and img')
            print 'Finish to compress html'
        except Exception as e:
            self.file.logger(self.log_path, 'Exception to compress html and img: {0}'.format(e.message))
            print 'Exception to compress html and img: {0}'.format(e.message)

        local_html_tmp_file = "{0}.tar.gz".format(self.temp_html_path)
        remote_html_tmp_file = "{0}//html.tar.gz".format(self.remote_html_path)
        local_img_tmp_file = "{0}.tar.gz".format(self.temp_img_path)
        remote_img_tmp_file = "{0}//img.tar.gz".format(self.remote_img_path)
        if self.doraemon.isFileExists(local_html_tmp_file):
            try:
                self.file.logger(self.log_path, 'Start upload html for: {0} '.format(self.name))
                print 'Start upload html for: {0} '.format(self.name)
                self.transer.singleUpload(local_html_tmp_file,
                                          remote_html_tmp_file,
                                          self.host_name,
                                          self.user_name,
                                          self.password,
                                          self.port)
                self.file.logger(self.log_path, 'Finished upload html for: {0} '.format(self.name))
                print 'Finished upload html for: {0} '.format(self.name)
            except Exception as e:
                self.file.logger(self.log_path, 'Exception to upload html: {0}'.format(e.message))
                print 'Exception to upload html: {0}'.format(e.message)
        else:
            print 'No html to upload'

        if self.doraemon.isFileExists(local_img_tmp_file):
            try:
                self.file.logger(self.log_path, 'Start upload image for: {0} '.format(self.name))
                print 'Start upload image for: {0} '.format(self.name)
                self.transer.singleUpload(local_img_tmp_file,
                                          remote_img_tmp_file,
                                          self.host_name,
                                          self.user_name,
                                          self.password,
                                          self.port)
                self.file.logger(self.log_path, 'Finished upload image for: {0} '.format(self.name))
                print 'Finished upload image for: {0} '.format(self.name)
            except Exception as e:
                self.file.logger(self.log_path, 'Exception to upload img: {0}'.format(e.message))
                print 'Exception to upload img: {0}'.format(e.message)
        else:
            print 'No image to upload'

if __name__ == '__main__':
    WeixinTalk=WeixinTalk()
    WeixinTalk.start_upload()