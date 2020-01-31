#coding:utf-8
import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
import urlparse
import re
from Tegenaria.tSpider.tSpider.middlewares.camelBone import CamelBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Camel():
    def __init__(self):
        self.doraemon = Doraemon()
        self.camelBone = CamelBone('adquan', callback=self.parse)
        self.regx = re.compile("\/post-[0-9]{0,}-[0-9]{0,}\.html")
        self.badkeys = []
        self.goodkeys = []

    def parse(self, current_url, html):
        results = []
        href_items = []
        href_items0_1 = html.xpath(".//a")
        self.current_url = current_url
        self.html = html
        if len(href_items0_1) > 0:
            href_items += href_items0_1
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
                short_url_parts = re.split(r'[., /, _, %, ", ?, =]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                title = ""
                title0_1 = item.xpath(".//text()")
                if len(title0_1) > 0:
                    title = ''.join(title0_1).strip()
                    print title
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