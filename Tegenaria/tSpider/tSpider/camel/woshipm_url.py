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
        self.camelBone = CamelBone('woshipm', callback=self.parse)
        self.badkeys = []
        self.goodkeys = []
        self.catagories = ['ucd', 'it', 'pmd', 'pd', 'operate', 'rp',
                           'evaluating', 'zhichang', 'chuangye', 'marketing', 'ai', 'blockchain']

    def getCatagoryKey(self, url):
        try:
            for key in self.catagories:
                regx = re.compile("^(?:http)s?://www.woshipm.com/" + key + "/[0-9]{0,}.html")
                isMatched = regx.match(url)
                if isMatched is not None:
                    return key
            return None
        except Exception as e:
            print ("Exception to match: {0} for {1}".format(url, e))
            return None

    def parse(self, current_url, html):
        results = []
        href_items = html.xpath(".//a")
        for item in href_items:
            href = item.xpath("@href")
            valid = True
            if len(href) == 0:
                continue
            href_url = href[0]
            matchedKey = self.getCatagoryKey(href_url)
            if matchedKey is None:
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
                id = short_url_parts[short_url_parts.index(matchedKey) + 1]
                url = urlparse.urljoin(current_url, href_url)
                title = ""
                title_list1 = item.xpath(".//text()")
                if len(title_list1) > 0:
                    title = ''.join(title_list1).strip()
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