#coding:utf-8
#------requirement------
#selenium-3.14.1
#------requirement------
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from logging import getLogger
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from settings import Settings

class SeleniumMiddleware(object):
    def init(self, timeout=None, executable_path=None):
        self.logger = getLogger(__name__)
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

    def chrome_request(self, url):
        self.init(timeout=Settings.SELENIUM_TIMEOUT, executable_path=Settings.CHROMEDRIVER_PATH)
        try:
            self.logger.debug('--------Chrome is Starting--------')
            self.browser.get(url)
            return self.browser

        except TimeoutException:
            self.logger.debug('--------Chrome is Timeout--------')
            self.close()
            self.init()