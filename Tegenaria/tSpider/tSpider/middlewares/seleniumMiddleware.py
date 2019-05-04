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
    def __init__(self):
        self.settings = Settings()
        self.settings.CreateCommonSettings()

    def init(self, timeout=None, executable_path=None, proxy=None):
        self.file = FileIOMiddleware()
        self.timeout = timeout
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if proxy is not None:
            chrome_options.add_argument('--proxy-server=http://{0}'.format(proxy))
        self.browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        self.load_timeout = self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def close(self):
        self.browser.close()
        self.browser.quit()
        del self.browser, self.file, self.timeout, self.load_timeout, self.wait
        gc.collect()

    def chrome_request(self, url, log_path, proxy):
        self.init(timeout=self.settings.SELENIUM_TIMEOUT, executable_path=self.settings.CHROMEDRIVER_PATH, proxy=proxy)
        try:
            self.file.logger(log_path, 'Starting Chrome for: {0}'.format(url))
            self.browser.get(url)
            return self.browser
        except TimeoutException:
            self.file.logger(log_path, 'Chrome timeout for: {0}'.format(url))
            self.close()
            return self.browser
        finally:
            self.close()
            return self.browser