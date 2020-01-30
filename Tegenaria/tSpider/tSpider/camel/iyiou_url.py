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
        self.camelBone = CamelBone('iyiou', callback=self.parse)
        self.regx = re.compile("^(?:http)s?:\/\/www\.iyiou\.com\/(p?|breaking|intelligence)\/[a-z0-9]{0,}\.html")
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
            href_url = str(href[0])
            valid = self.doraemon.isUrlValid(href_url,
                                             self.goodkeys,
                                             self.badkeys,
                                             self.regx.match(href_url),
                                             valid)
            if valid:
                short_url_parts = re.split(r'[., /, _]', href_url)
                id = short_url_parts[len(short_url_parts) - 2]
                url = urlparse.urljoin(current_url, href_url)
                title = ""
                title_list1 = item.xpath("@title")
                title_list2 = item.xpath(".//h2//text()")
                title_list3 = item.xpath(".//p//text()")
                if len(title_list1) > 0:
                    title_tmp = ''.join(title_list1).strip()
                    if self.doraemon.isEmpty(title_tmp) is False:
                        title = title_tmp
                        title.strip()
                        print title
                if len(title_list2) > 0:
                    title_tmp = ''.join(title_list2).strip()
                    if self.doraemon.isEmpty(title_tmp) is False:
                        title = title_tmp
                        title.strip()
                        print title
                if len(title_list3) > 0:
                    title_tmp = ''.join(title_list3).strip()
                    if self.doraemon.isEmpty(title_tmp) is False:
                        title = title_tmp
                        title.strip()
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