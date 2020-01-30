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
        self.camelBone = CamelBone('huxiu', callback=self.parse)
        self.regx = re.compile("\/article\/[0-9]{0,}\.html")
        self.badkeys = ['video']
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
            isValidUrl = self.regx.match(href_url)
            if isValidUrl is None:
                print 'Invalid url for not match: {0}'.format(href_url)
                continue
            short_url = href[0]
            id = str(filter(str.isdigit, short_url.encode('gbk')))
            url = urlparse.urljoin(current_url, short_url)
            for good in self.goodkeys:
                if valid == True:
                    continue
                if good in url:
                    valid = True
            for bad in self.badkeys:
                if valid == False:
                    continue
                if bad in url:
                    valid = False
            if valid:
                title = ''
                title_list1 = item.xpath(".//*[contains(@class, 'multi-line-overflow')]//text()")
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