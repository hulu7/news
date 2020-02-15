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
    def __init__(self, siteinfo=None):
        self.siteinfo = siteinfo
        if self.siteinfo == None:
            return
        self.doraemon = Doraemon()
        self.camelBone = CamelBone(self.siteinfo, callback=self.parse)
        self.regx = self.siteinfo.url_match
        self.badkeys = self.siteinfo.bad_keys
        self.goodkeys = self.siteinfo.good_keys
        self.url_id_tag = self.siteinfo.url_id_tag
        self.url_title_match = self.siteinfo.url_title_match

    def parse(self, current_url, html):
        results = []
        href_items = []
        self.current_url = current_url
        self.html = html
        for item in self.siteinfo.href_items:
            href_item = html.xpath('{0}'.format(item.regx))
            if href_item > 0:
                href_items += href_item
        for item in href_items:
            for url_item in self.siteinfo.href:
                href = item.xpath('{0}'.format(url_item.regx))
                valid = True
                if len(href) == 0:
                    continue
                href_url = href[0]
                valid = self.doraemon.isUrlValid(href_url,
                                                 self.goodkeys,
                                                 self.badkeys,
                                                 self.regx,
                                                 valid)
                if valid:
                    short_url_parts = re.split(r'[., /, _, %, ", ?, =, &, #]', href_url)
                    id = self.doraemon.getUrlId(short_url_parts, self.url_id_tag)
                    if id == None:
                        print 'Id is empty for url: {0}'.format(current_url)
                        continue
                    url = urlparse.urljoin(current_url, href_url)
                    title = ""
                    for title_item in self.url_title_match:
                        title_temp = item.xpath('{0}'.format(title_item.regx))
                        if self.doraemon.isEmpty(title_temp) is False:
                            effective_index = title_item.index
                            if effective_index == -1:
                                title = ''.join(title_temp).strip()
                            else:
                                title = ''.join(title_temp[effective_index]).strip()
                            if self.doraemon.isEmpty(title) is False:
                                print title
                                break
                    uniCodeTest = title.split()
                    if self.doraemon.isTitleEmpty(title, url) or self.doraemon.isEmpty(uniCodeTest):
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