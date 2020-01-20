#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../')
import urlparse
from middlewares.camelBone import CamelBone
from middlewares.doraemonMiddleware import Doraemon

class Camel():
    def __init__(self):
        self.doraemon = Doraemon()
        self.camelBone = CamelBone('chuansongme', callback=self.parse)
        self.badkeys = []
        self.goodkeys = []

    def parse(self, current_url, html):
        results = []
        href_items = html.xpath(".//*[contains(@class,'question_link')]")
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            id = href_url.replace('/n/', '').strip()
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
                url = urlparse.urljoin(current_url, href_url).strip()
                title = ""
                title_list1 = item.xpath(".//text()")
                if len(title_list1) > 0:
                    title = title_list1[0].strip()
                    print title
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