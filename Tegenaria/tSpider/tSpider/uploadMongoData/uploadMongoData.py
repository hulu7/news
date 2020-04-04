# -*- coding:utf-8 -*-
import sys
reload(sys)
import os
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class UploadMongoData():
    def __init__(self):
        self.settings = Settings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.log_path = self.settings.LOG_PATH
        self.doraemon.createFilePath(self.log_path)

    def startUpload(self):
        fromFile = self.settings.LOCAL_MONGO_DATA_PATH
        toFile = self.settings.REMOTE_MONGO_DATA_PATH
        if not os.path.exists(fromFile):
            print 'no mongo data file to upload'
            return
        while os.path.exists(fromFile):
            try:
                if self.doraemon.sshUpload(self.settings.IP_WEBSERVER0,
                                           self.settings.PORT_WEBSERVER0,
                                           self.settings.USER_ROOT_WEBSERVER0,
                                           self.settings.USER_ROOT_PASSWORD_WEBSERVER0,
                                           fromFile,
                                           toFile):
                    self.doraemon.deleteFile(fromFile)
                    message1 = 'Success to upload mongo data file: {0}'.format(fromFile)
                    print message1
                    self.file.logger(self.log_path, message1)
            except Exception as e:
                message2 = 'Exception {0} to upload mongo data file: {1}'.format(e.message, fromFile)
                print message2
                self.file.logger(self.log_path, message2)

if __name__ == '__main__':
    upload=UploadMongoData()
    upload.startUpload()