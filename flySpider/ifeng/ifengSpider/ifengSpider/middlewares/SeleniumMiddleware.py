#coding:utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import HtmlResponse
from logging import getLogger

class SeleniumMiddleware(object):

    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.load_timeout = self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用Chromedriver抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        try:
            self.logger.debug('--------Chrome is Starting--------')
            self.browser.get(request.url)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            self.logger.debug('--------Chrome is Timeout--------')
            self.browser.close()
            self.__init__()
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('CHROMEDRIVER_SERVICE_ARGS'))