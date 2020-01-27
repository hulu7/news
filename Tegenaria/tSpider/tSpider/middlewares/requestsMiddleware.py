#coding:utf-8
#------requirement------
#requests-2.6.0
#------requirement------
import requests
import random
import sys
reload(sys)
import gc
from multiprocessing.pool import ThreadPool as Pool
sys.setdefaultencoding('utf8')
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
        except Exception as e:
            self.file.logger(self.settings.LOG_PATH, 'Requests Timeout: {0}'.format(str(e.message)))

    def run_task(self, url_title=[], callback=callable, headers=None, host=None):
        self.file.logger(self.log_path, 'Start: {0}'.format(url_title[0]))
        print 'Start: {0}'.format(url_title[0])
        response = self.requests_request(url_title[0], headers, host, url_title[0])
        try:
            callback({'response': response, 'request_url': url_title[0], 'request_title': url_title[1]})
        except Exception as e:
            self.file.logger(self.log_path, 'Exception: {0} for {1}'.format(e.message, url_title[0]))
            print 'Exception: {0} for {1}'.format(e.message, url_title[0])
            del response, self.requests_request
            gc.collect()
        self.file.logger(self.log_path, 'End: {0}'.format(response.url))
        print 'End: {0}'.format(response.url)
        del response, self.requests_request
        gc.collect()

    def start_requests(self, url_titles, processes, log_path, headers, host, proxy, callback=callable):
        self.file = FileIOMiddleware()
        self.content = []
        self.log_path = log_path
        self.proxy = proxy
        process = Pool(processes)
        for url_title in url_titles:
            process.apply_async(self.run_task, args=(url_title, callback, headers, host))
        process.close()
        process.join()
        self.file.logger(self.log_path, 'Done')
        print 'Done'
        del self.file, process
        gc.collect()
