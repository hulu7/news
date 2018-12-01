# -*- coding: utf-8 -*-
#------requirement------
#gevent-1.3.7
#selenium-3.14.1
#Scrapy-1.5.1
#
#
#------requirement------
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from settings import Settings
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from middlewares.fileIO import File

class Request():

    def init(self, timeout=None, executable_path=None):
        self.timeout = timeout
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        self.load_timeout = self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def close(self, browsers):
        for browser in browsers:
            browser.close()

    def request(self, urls):
        self.file = File()
        pool = Pool(Settings.MAX_POOL_SIZE)
        return pool.map(self.run_task, urls)

    def run_task(self, url):
        self.init(timeout=Settings.SELENIUM_TIMEOUT, executable_path=Settings.CHROMEDRIVER_PATH)
        self.file.logger(Settings.LOG_PATH, 'getting --> %s' %url)
        print 'getting ---> %s' %url
        try:
            self.browser.get(url)
        except TimeoutException:
            print TimeoutException
            self.file.logger(Settings.LOG_PATH, str(TimeoutException))
        self.file.logger(Settings.LOG_PATH, 'url:%s ---> finished' % url)
        print 'url:%s ---> finished' % url
        return self.browser.current_url


if __name__ == '__main__':
    r = Request()
    # urls = ['https://www.huxiu.com', 'http://www.ifeng.com/', 'http://www.ce.cn/']
    urls = ['http://news.ifeng.com/a/20181122/60170977_0.shtml', 'http://news.ifeng.com/a/20181122/60170867_0.shtml', 'http://news.ifeng.com/a/20181122/60170530_0.shtml']
    result = r.request(urls)
    print result