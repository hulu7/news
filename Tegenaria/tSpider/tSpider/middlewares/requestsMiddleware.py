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
    def init(self, headers=None, host=None, referer=None):
        self.file = FileIOMiddleware()
        self.requests = requests
        self.headers = headers
        if headers is None:
            self.headers = {}
            self.headers['Accept'] = Settings.ACCEPT
            self.headers['Accept-Encoding'] = Settings.ACCEPT_ENC0DING
            self.headers['Accept-Language'] = Settings.ACCEPT_LANGUAGE
            self.headers['Cache-Control'] = Settings.CACHE_CONTROL
            self.headers['Connection'] = Settings.CONNECTION
            self.headers['Host'] = host
            self.headers['Upgrade-Insecure-Requests'] = Settings.UPGRADE_INSECURE_REQUESTS
            self.headers['Referer'] = referer
            self.headers['Pragma'] = Settings.PRAGMA
            self.headers['User-Agent'] = Settings.USER_AGENTS[random.randint(0, len(Settings.USER_AGENTS) - 1)]

    def requests_request(self, url, headers=None, host=None, referer=None):
        self.init(headers=headers, host=host, referer=referer)
        try:
            self.file.logger(Settings.LOG_PATH, 'Starting Requests')
            res = self.requests.get(url=url, headers=self.headers)
            return res
        except Exception, e:
            self.file.logger(Settings.LOG_PATH, 'Requests Timeout: {0}'.format(str(e)))
            del self.file, self.requests, self.headers
            gc.collect()