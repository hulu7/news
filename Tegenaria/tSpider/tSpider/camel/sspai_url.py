#coding:utf-8
import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
import urlparse
import re
from Tegenaria.tSpider.tSpider.middlewares.camelBone import CamelBone
from Tegenaria.tSpider.tSpider.middlewares.noNameBone import NoNameBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import noNameDto

class Camel():
    def __init__(self):
        self.doraemon = Doraemon()
        self.camelBone = CamelBone('sspai', callback=self.parse)
        self.regx = re.compile("/post/[0-9]{0,}")
        self.badkeys = []
        self.goodkeys = []
        self.noNameDto = noNameDto('', [])
        self.noNameBone = NoNameBone('sspai', callback=self.parseAuthors)
        self.author_regx = re.compile("/u/[0-9]{0,}[a-z]{0,}[A-Z]{0,}")
        self.isReadyToParseAuthore = False

    def parseAuthors(self):
        if self.isReadyToParseAuthore == False:
            print 'Not ready to parse author for {0}'.format('sspai')
            return
        href_items = self.html.xpath(".//*[contains(@class, 'pic_box')]//a")
        self.noNameDto.page_url = self.current_url
        for item in href_items:
            href = item.xpath("@href")
            if len(href) == 0:
                continue
            href_url = href[0]
            isValidUrl = self.author_regx.match(href_url)
            if isValidUrl is None:
                print 'Invalid author for not match: {0}'.format(href_url)
                continue
            url = urlparse.urljoin(self.current_url, href_url)
            if url not in self.noNameDto.authors:
                self.noNameDto.authors.append(url)
        return self.noNameDto

    def parse(self, current_url, html):
        self.isReadyToParseAuthore = True
        results = []
        href_items = html.xpath(".//*[contains(@class, 'pc_card')]")
        self.current_url = current_url
        self.html = html
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
                short_url_parts = re.split(r'[., /, _, %, ", ?, =]', href_url)
                id = short_url_parts[short_url_parts.index('post') + 1]
                url = urlparse.urljoin(current_url, href_url)
                title = ""
                title_list1 = item.xpath(".//*[contains(@class, 'title')]//text()")
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
    camel.noNameBone.store()