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
        self.camelBone = CamelBone('yicai', callback=self.parse)
        self.regx = re.compile("\/news\/[0-9]{0,}\.html")
        self.badkeys = ['daohang', 'video']
        self.goodkeys = ['']

    def parse(self, current_url, html):
        results = []
        href_items = html.xpath(".//a")
        if len(href_items) == 0:
            return
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
                title_content0_1 = item.xpath(".//div/h2/text()")
                title_content0_2 = item.xpath(".//div/h3/span/text()")
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                if len(title_content0_1) != 0:
                    title = title_content0_1[0]
                elif len(title_content0_2) != 0:
                    title = title_content0_2[0]
                else:
                    title = ""
                if len(str(filter(str.isdigit, id))) != 0 and title is not None:
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