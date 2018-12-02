#coding:utf-8
#------requirement------
#selenium-3.14.1
#------requirement------
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware

class SeleniumMiddleware(object):
    def init(self, timeout=None, executable_path=None):
        self.file = FileIOMiddleware()
        self.timeout = timeout
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        self.load_timeout = self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def close(self):
        self.browser.close()
        self.browser.quit()
        del self.browser, self.file, self.timeout, self.load_timeout, self.wait
        gc.collect()

    def chrome_request(self, url):
        self.init(timeout=Settings.SELENIUM_TIMEOUT, executable_path=Settings.CHROMEDRIVER_PATH)
        try:
            self.file.logger(Settings.LOG_PATH, 'Starting Chrome for: %s' % url)
            self.browser.get(url)
            return self.browser
        except TimeoutException:
            browser = self.browser
            self.file.logger(Settings.LOG_PATH, 'Chrome timeout for: % s' % url)
            self.close()
            return browser