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
    def __init__(self):
        self.settings = Settings()
        self.settings.CreateCommonSettings()

    def init(self, headers=None, host=None, referer=None):
        self.file = FileIOMiddleware()
        self.requests = requests
        self.headers = headers
        if headers is None:
            self.headers = {}
            self.headers['Accept'] = self.settings.ACCEPT
            self.headers['Accept-Encoding'] = self.settings.ACCEPT_ENC0DING
            self.headers['Accept-Language'] = self.settings.ACCEPT_LANGUAGE
            self.headers['Cache-Control'] = self.settings.CACHE_CONTROL
            self.headers['Connection'] = self.settings.CONNECTION
            self.headers['Host'] = host
            self.headers['Upgrade-Insecure-Requests'] = self.settings.UPGRADE_INSECURE_REQUESTS
            self.headers['Referer'] = referer
            self.headers['Pragma'] = self.settings.PRAGMA
            self.headers['User-Agent'] = self.settings.USER_AGENTS[random.randint(0, len(self.settings.USER_AGENTS) - 1)]

    def requests_request(self, url, headers=None, host=None, referer=None):
        self.init(headers=headers, host=host, referer=referer)
        try:
            self.file.logger(self.settings.LOG_PATH, 'Starting Requests')
            res = self.requests.get(url=url, headers=self.headers)
            return res
        except Exception, e:
            self.file.logger(self.settings.LOG_PATH, 'Requests Timeout: {0}'.format(str(e)))
            del self.file, self.requests, self.headers
            gc.collect()