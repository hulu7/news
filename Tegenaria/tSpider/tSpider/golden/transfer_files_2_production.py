#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import datetime
import json
from shutil import copyfile
import os
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon
from middlewares.requestsMiddleware import RequestsMiddleware

class TransferToProduction():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.request = RequestsMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.settings.LOG_PATH)
        self.doraemon.createFilePath(self.temp_folder_html)
        self.doraemon.createFilePath( self.temp_folder_img)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('weixin')
        self.source = settings_name['SOURCE_NAME']
        self.work_path_prd2 = settings_name['WORK_PATH_PRD2']
        self.mongo = settings_name['MONGO_URLS']
        self.name = settings_name['NAME']
        self.finished_content_path = settings_name['FINISHED_CONTENT_PATH']
        self.finished_img_path = settings_name['FINISHED_IMG_PATH']
        self.finished_processed_html_path = settings_name['FINISHED_PROCESSED_HTML_PATH']
        self.temp_folder_html = self.settings.TEMP_FOLDER_HTML
        self.temp_folder_img = self.settings.TEMP_FOLDER_IMG
        self.log_path = self.settings.LOG_PATH
        self.today = self.settings.TODAY

    def start_transfer(self):
        print 'Start {0} transfer'.format(self.name)
        new_ids = self.doraemon.readNewImageIds(self.doraemon.bf_finished_temp_weixin, self.finished_content_path)
        for id in new_ids:
            self.file.logger(self.log_path, 'Start transfer image: {0}'.format(id))
            regx_img_file = re.compile(id)
            for f in os.listdir(self.finished_img_path):
                isValidImage = regx_img_file.match(f)
                if isValidImage is None:
                    print 'Invalid image for not match: {0}'.format(f)
                    continue
                from_img_path = "{0}//{1}".format(self.finished_img_path, f)
                to_img_path = "{0}//{1}".format(self.temp_folder_img, f)
                is_from_path_exists = os.path.exists(from_img_path)
                if is_from_path_exists is False:
                    self.file.logger(self.log_path, 'img of {0} not exits.'.format(f))
                    continue
                copyfile(from_img_path, to_img_path)
                print 'Finished to transfer image {0}'.format(f)
            self.file.logger(self.log_path, 'Start transfer html: {0}'.format(id))
            from_path = "{0}//{1}.html".format(self.finished_processed_html_path, id)
            to_path = "{0}//{1}.html".format(self.temp_folder_html, id)
            is_from_path_exists = os.path.exists(from_path)
            if is_from_path_exists is False:
                self.file.logger(self.log_path, 'html of {0} not exits.'.format(id))
                continue
            copyfile(from_path, to_path)
            print 'Finished to transfer html {0}'.format(id)
            self.doraemon.storeFinished(self.doraemon.bf_finished_temp_weixin, id)
            print 'Finished to transfer {0}'.format(id)

if __name__ == '__main__':
    TransferToProduction=TransferToProduction()
    TransferToProduction.start_transfer()