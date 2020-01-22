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
        self.camelBone = CamelBone('cankaoxiaoxi', callback=self.parse)
        self.badkeys = ['mid', 'about', 'photo', 'index']
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
            if 'html' not in href_url:
                continue
            if len(self.goodkeys) > 0:
                for good in self.goodkeys:
                    if valid == True:
                        continue
                    if good in href_url:
                        valid = True
            if len(self.badkeys) > 0:
                for bad in self.badkeys:
                    if valid == False:
                        continue
                    if bad in href_url:
                        valid = False
            if valid:
                short_url_parts = re.split(r'[., /, _, ?, #]', href_url)
                if len(short_url_parts) < 2:
                    continue
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                title = ''
                title0_1 = item.xpath(".//div/h3/text()")
                title0_2 = item.xpath(".//h3/text()")
                title0_3 = item.xpath("@title")
                if self.doraemon.isEmpty(title0_1) is False:
                    title = ''.join(title0_1)
                if self.doraemon.isEmpty(title0_2) is False:
                    title = ''.join(title0_2)
                if self.doraemon.isEmpty(title0_3) is False:
                    title = ''.join(title0_3)
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