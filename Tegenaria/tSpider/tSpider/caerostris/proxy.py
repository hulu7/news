# coding:utf-8
# ------requirement------
# lxml-3.2.1
# numpy-1.15.2
# ------requirement------

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

class Proxy():

    def __init__(self):
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
    def getSettings(self):
        self.proxy_pool = Settings.PROXY_POOL
        self.valid_proxy_sogo = Settings.VALID_PROXY_SOGO_URL
        self.valid_proxy_gongzhonghao = Settings.VALID_PROXY_GONGZHONGHAO_URL

    def refreshProxy(self):
        response = requests.get(self.proxy_pool)
        proxy_pool = eval(response.content)
        valid_proxy = []
        valid_proxy.append(self.valid_proxy_sogo)
        valid_proxy.append(self.valid_proxy_gongzhonghao)
        print 'Start refresh proxy.'

        for proxy in proxy_pool:
            ip_port = '{0}:{1}'.format(proxy[0], proxy[1])
            for vp in valid_proxy:
                self.doraemon.hashSet(vp, ip_port, ip_port)
        print 'Finished refresh proxy.'


if __name__ == '__main__':
    Proxy = Proxy()
    Proxy.refreshProxy()