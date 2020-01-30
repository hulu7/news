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
        self.camelBone = CamelBone('xueqiu', callback=self.parse)
        self.regx = re.compile("\/[0-9]{1,}\/[0-9]{1,}")
        self.badkeys = []
        self.goodkeys = []

    def parse(self, current_url, html):
        results = []
        href_items = []
        href_items0_1 = html.xpath(".//*[contains(@class, 'timeline__item__content')]//a")
        href_items0_2 = html.xpath(".//*[contains(@class, 'home__timeline__item')]//a")
        href_items0_3 = html.xpath(".//*[contains(@class, 'AnonymousHome_home__timeline__item_3vU')]//a")
        if len(href_items0_1) > 0 :
            href_items += href_items0_1
        if len(href_items0_2) > 0:
            href_items += href_items0_2
        if len(href_items0_3) > 0:
            href_items += href_items0_3
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            isValidUrl = self.regx.match(href_url)
            if isValidUrl is None:
                print 'Invalid url for not match: {0}'.format(href_url)
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
                short_url_parts = re.split(r'[., /, _, %, "]', href_url)
                id = short_url_parts[len(short_url_parts) - 1]
                url = urlparse.urljoin(current_url, href_url)
                title = ""
                title_list1 = item.xpath(".//text()")
                if len(title_list1) > 0:
                    title = ''.join(title_list1).strip()
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