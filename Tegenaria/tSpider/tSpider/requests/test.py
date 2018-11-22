# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from settings import Settings
from middlewares.seleniumMiddleware import SeleniumMiddleware
from middlewares.fileIO import File
from coroutine import Request

urls = ['http://news.ifeng.com/a/20181121/60169573_0.shtml', 'http://news.ifeng.com/a/20181122/60170867_0.shtml',
        'http://news.ifeng.com/a/20181122/60170530_0.shtml', 'https://pl.ifeng.com/a/20181122/60170059_0.shtml']

request = Request()
requests = request.request(urls)
for req in requests:
    print req.current_url
request.close(requests)