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
        self.camelBone = CamelBone('ce', callback=self.parse)
        self.badkeys = ['tu', 'index']
        self.goodkeys = ['']

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
            for good in self.goodkeys:
                if valid == True:
                    continue
                if good in href_url:
                    valid = True
            for bad in self.badkeys:
                if valid == False:
                    continue
                if bad in href_url:
                    valid = False
            if valid:
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                title = item.text
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