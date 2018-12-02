#coding:utf-8
#------requirement------
#requests-2.6.0
#------requirement------
import requests
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class RequestsMiddleware():
    def init(self, headers=None):
        self.file = FileIOMiddleware()
        self.requests = requests
        self.headers = headers
        if headers is not None:
            self.headers['User-Agent'] = Settings.USER_AGENTS[random.randint(0, len(Settings.USER_AGENTS))]

    def requests_request(self, url, headers=None):
        self.init(timeout=Settings.SELENIUM_TIMEOUT, headers=headers)
        try:
            self.file.logger(Settings.LOG_PATH, 'Starting Requests')
            res = self.requests.get(url=url, headers=self.headers)
            return res
        except Exception, e:
            self.file.logger(Settings.LOG_PATH, 'Requests Timeout: ' + e)
            del self.file, self.requests, self.headers
            gc.collect()