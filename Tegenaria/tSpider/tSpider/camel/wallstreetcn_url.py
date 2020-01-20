#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../')
import urlparse
import re
from middlewares.camelBone import CamelBone
from middlewares.doraemonMiddleware import Doraemon

class Camel():
    def __init__(self):
        self.doraemon = Doraemon()
        self.camelBone = CamelBone('wallstreetcn', callback=self.parse)
        self.badkeys = ['vip', 'premium']
        self.goodkeys = ['articles']

    def parse(self, current_url, html):
        results = []
        href_items = html.xpath(".//a[contains(@class, 'title')]")
        if len(href_items) == 0:
            return
        for item in href_items:
            href = item.xpath("@href")
            valid = False
            if len(href) == 0:
                continue
            href_url = href[0]
            for good in self.goodkeys:
                if valid == True:
                    break
                if good in href_url:
                    valid = True
            for bad in self.badkeys:
                if valid == False:
                    continue
                if bad in href_url:
                    valid = False
            if valid:
                title_content0_1 = item.xpath(".//text()")
                if len(title_content0_1) == 0:
                    continue
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 1]
                url = urlparse.urljoin(current_url, href_url)
                if len(title_content0_1) != 0:
                    title = title_content0_1[0].strip()
                else:
                    title = ""
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