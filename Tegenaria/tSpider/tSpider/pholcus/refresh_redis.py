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
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon
from middlewares.requestsMiddleware import RequestsMiddleware

class RefreshRedis():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.request = RequestsMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('weixin')
        self.name = settings_name['NAME']
        self.log_path = self.settings.LOG_PATH_PRD2
        self.redis_refresh_path = settings_name['REDIS_REFRESH_PATH']
        self.refresh_redis_interval = self.settings.REFRESH_REDIS_INTERVAL
        self.finished_weixin_url_id = self.settings.FINISHED_WEIXIN_URL_ID

    def start(self):
        if self.doraemon.isExceedRestartInterval(self.redis_refresh_path, self.refresh_redis_interval) is False:
            return
        self.file.logger(self.log_path, 'Start refresh redis')
        print 'Start refresh redis'
        key = '{0}0'.format(self.finished_weixin_url_id)
        self.doraemon.delKey(key)
        self.file.logger(self.log_path, 'Finished to refresh redis')
        print 'Finished to refresh redis'

if __name__ == '__main__':
    RefreshRedis=RefreshRedis()
    RefreshRedis.start()