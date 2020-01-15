#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
import urlparse
import re
from Tegenaria.tSpider.tSpider.middlewares.camelBone import CamelBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Camel():
    def __init__(self):
        self.doraemon = Doraemon()
        self.camelBone = CamelBone('jingji21', callback=self.parse)

    def parse(self, current_url, html):
        results = []
        href_items = html.xpath(".//*[contains(@class,'news_list')]/a")
        for item in href_items:
            short_url = item.xpath("@href")[0]
            if 'html' not in short_url:
                continue
            short_url_parts = re.split(r'[., /, _]', short_url)
            id = short_url_parts[len(short_url_parts) - 2]
            url = urlparse.urljoin(current_url, short_url)
            title = ''.join(item.xpath(".//*[contains(@class,'news_title')]/text()"))
            results.append(self.doraemon.createCamelData(
                title.strip(),
                url.strip(),
                id.strip(),
                self.camelBone.today,
                self.camelBone.source
            ))
        return results

if __name__ == '__main__':
    camel = Camel()
    camel.camelBone.start()