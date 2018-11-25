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

# from items import HuxiuItem

urls = ['https://www.huxiu.com/article/273257.html', 'https://www.huxiu.com/article/273262.html']

def store_data(data):
    mongo=MongoMiddleware()
    mongo.insert(Settings.MONGO_HUXIU, data)

def show_data(response):
    html = etree.HTML(response.page_source)
    title = html.xpath(".//*[contains(@class,'t-h1')]/text()")[0].strip()
    comment_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'article-pl pull-left')]/text()")[0].encode('gbk')))
    share_number = str(filter(str.isdigit, html.xpath(".//*[contains(@class, 'article-share pull-left')]/text()")[0].encode('gbk')))
    image_url = html.xpath(".//*[contains(@class, 'article-img-box')]/img/@src")[0]
    url = response.current_url
    content = ''.join(html.xpath(".//div[contains(@class, 'article-content-wrap')]/p/text()"))
    time = html.xpath(".//*[@class='article-time pull-left']/text()")[0]
    author_url = urlparse.urljoin(response.current_url, html.xpath(".//*[@class='author-name']/a/@href")[0])
    author_name = html.xpath(".//*[@class='author-name']/a/text()")[0]
    id = filter(str.isdigit, response.current_url.encode('gbk'))
    data = {
        'title':title,
        'comment_number': comment_number,
        'share_number': share_number,
        'image_url': image_url,
        'url': url,
        'time': time,
        'author_url': author_url,
        'author_name': author_name,
        'id': id
    }
    print title
    store_data(data)

request = BrowserRequest()
content = request.start_chrome(urls, 1, callback=show_data)
print content