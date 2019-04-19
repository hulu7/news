# coding:utf-8
# ------requirement------
# lxml-3.2.1
# numpy-1.15.2
# ------requirement------
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import urlparse
import re
import requests
import time

sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from browserRequest import BrowserRequest
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon
from middlewares.requestsMiddleware import RequestsMiddleware

class SogoAccount():
    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.requests = RequestsMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)
        self.doraemon.createFilePath(self.settings.LOG_PATH)

    def getSettings(self):
        settings_name = self.settings.CreateSettings('sogo')
        self.work_path_prd2 = settings_name['WORK_PATH_PRD2']
        self.mongo = settings_name['MONGO_URLS']
        self.name = settings_name['NAME']
        self.max_pool_size = settings_name['MAX_POOL_SIZE']
        self.log_path = self.settings.LOG_PATH_PRD2
        self.urls = settings_name['URLS']
        self.restart_path = settings_name['RESTART_PATH']
        self.restart_interval = settings_name['RESTART_INTERVAL']
        self.valid_proxy_pool_sogo_account = self.settings.VALID_PROXY_POOL_SOGO_ACCOUNT
        self.invalid_proxy_pool_sogo_account= self.settings.INVALID_PROXY_POOL_SOGO_ACCOUNT
        self.finished_sogo_account = self.settings.FINISHED_SOGO_ACCOUNT
        self.regx = re.compile("[0-9]{1,}.[0-9]{1,}.[0-9]{1,}.[0-9]{1,}:[0-9]{1,}")

    def getProxy(self):
        url = "http://ip.16yun.cn:817/myip/pl/c167cc62-6ad5-4876-bfd8-0cc423dab398/?s=wygafjcqjv&u=hellobee&count=2"
        # url = "http://129.28.124.247:43059/get_ip.php?key=908299fbaefcacef4eb2c9e6ea18c5f2"
        response = self.requests.requests_request(url, headers=None, host="ip.16yun.cn", referer="ip.16yun.cn")
        proxy_list = response.text.strip().split('\n')
        for proxy in proxy_list:
            ip = proxy.strip()
            isValidIp = self.regx.match(ip)
            if self.doraemon.isEmpty(ip) is False and isValidIp is not None:
                self.file.logger(self.log_path, "Proxy: {0} is available.".format(ip))
                print "Proxy: {0} is available.".format(ip)
                try:
                    self.doraemon.hashSet(self.valid_proxy_pool_sogo_account, ip, ip)
                except Exception, e:
                    print "Exception to set redis for available sogo account of ip: {0}: {1}.".format(ip,e)
                    self.file.logger(self.log_path, "Exception to set redis for available sogo account of ip: {0}: {1}.".format(ip,e))
            else:
                self.file.logger(self.log_path, 'Fail to get proxy for sogo account.')
                print "Fail to get proxy for sogo account."

    def parse(self, response):
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        html = etree.HTML(response['response'].page_source)
        key = response['request_title']
        href_item = html.xpath(".//*[contains(@uigs, 'account_name_0')]/@href")
        if len(href_item) == 0:
            print 'Blocked and change for another proxy.'
            self.doraemon.hashSet(self.invalid_proxy_pool_sogo_account, self.proxy, self.proxy)
            self.doraemon.delHashSet(self.valid_proxy_pool_sogo_account, self.proxy)
            all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_pool_sogo_account))
            if len(all_valid_proxy) == 0:
                print 'The proxy pool is empty and get proxy again.'
                self.file.logger(self.log_path, 'The proxy pool is empty and get proxy again.')
                self.getProxy()
            all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_pool_sogo_account))
            self.proxy = all_valid_proxy.pop()
            return
        href = href_item[0]
        url = urlparse.urljoin(current_url, href)
        self.doraemon.hashSet(self.name, key, url)
        self.doraemon.hashSet(self.finished_sogo_account, key, key)
        print 'Finished for {0}'.format(key)
        self.current_url.pop()
        if len(self.new_urls) > 0:
            new_url = self.new_urls.pop()
            print 'Start next: {0}'.format(new_url[0])
            self.current_url.append(new_url)
        print 'End to parse {0}, url: {1}'.format(key, href_item[0])

    def start_requests(self):
        if self.doraemon.isExceedRestartInterval(self.restart_path, self.restart_interval) is False:
            return
        self.file.logger(self.log_path, 'Start {0} requests'.format(self.name))
        print 'Start {0} requests'.format(self.name)

        try:
            self.getProxy()
        except Exception, e:
            self.file.logger(self.settings.LOG_PATH, 'Exception to get proxy: {0}'.format(str(e)))

        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_sogo_account))
        all_valid_proxy = list(self.doraemon.getAllHasSet(self.valid_proxy_pool_sogo_account))

        if self.doraemon.isEmpty(all_valid_proxy):
            self.file.logger(self.log_path, 'No available proxy for sogo account and return.')
            print "No available proxy for sogo account and return."
            return

        self.new_urls = []
        self.current_url = []

        keys = []
        content = self.file.readFromTxt(self.urls)
        keys_list = content.split('\n')

        for key in keys_list:
            if self.doraemon.isEmpty(key) is False:
                keys.append(key)

        self.proxy = all_valid_proxy.pop()
        for key in keys:
            if key not in all_finished_id:
                timestamp = '00'.join(str(time.time()).split('.'))
                tmp_url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query={0}&ie=utf8&_sug_=n&_sug_type_=".format(key)
                self.new_urls.append([tmp_url, key])

        request = BrowserRequest()
        if len(self.new_urls) > 0:
            self.current_url.append(self.new_urls.pop())
        else:
            print 'No more urls.'
        while len(self.current_url) > 0:
            print "Proxy :{0}".format(self.proxy)
            if len(self.new_urls) > 0:
                self.current_url.append(self.new_urls.pop())
            else:
                print 'No more urls.'
            request.start_chrome(self.current_url, self.max_pool_size, self.log_path, self.proxy, callback=self.parse)

        self.file.logger(self.log_path, 'End for requests of {0}.'.format(self.name))

if __name__ == '__main__':
    SogoAccount = SogoAccount()
    SogoAccount.start_requests()