# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from lxml import etree
import urlparse
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from settings import Settings
from middlewares.mongodbMiddleware import MongoMiddleware
import asyncio

loop = asyncio.get_event_loop()
host = 'http://www.huxiu.com'
urls_todo = {'/article/273257.html', '/article/19.html', '/article/20.html', '/article/21.html'}

request = BrowserRequest()
content = request.start_chrome(urls_todo, 1, callback=None)
print content