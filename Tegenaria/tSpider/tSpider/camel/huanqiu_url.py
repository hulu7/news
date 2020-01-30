#coding:utf-8
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
        self.camelBone = CamelBone('huanqiu', callback=self.parse)
        self.regx = re.compile("(http(s?):)?\/\/[a-zA-Z]{0,}\.huanqiu\.com\/article\/[0-9a-zA-Z]{0,}")
        self.badkeys = []
        self.goodkeys = []

    def parse(self, current_url, html):
        results = []
        href_items = html.xpath(".//a")
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            valid = self.doraemon.isUrlValid(href_url,
                                             self.goodkeys,
                                             self.badkeys,
                                             self.regx.match(href_url),
                                             valid)
            if valid:
                short_url_parts = re.split(r'[., /, _, ?]', href_url)
                id = short_url_parts[short_url_parts.index('article') + 1].strip()
                url = urlparse.urljoin(current_url, href_url).strip()
                title = ''
                title0_1 = item.xpath(".//*[contains(@class, 'news-title')]/text()")
                title0_2 = item.xpath(".//*[contains(@class, 'lunbo-title')]/text()")
                title0_3 = item.xpath(".//text()")
                if self.doraemon.isEmpty(title0_1) is False:
                    title = ''.join(title0_1).strip()
                if self.doraemon.isEmpty(title0_2) is False:
                    title = ''.join(title0_2).strip()
                if self.doraemon.isEmpty(title0_3) is False:
                    title = ''.join(title0_3).strip()
                if self.doraemon.isTitleEmpty(title, url):
                    continue
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