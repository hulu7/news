# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from ifengUrlSpider.items import IfengUrlspiderToMongodbItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re

class IfengUrlSpider(CrawlSpider):
    name = 'ifengUrl'
    allowed_domains = ["ifeng.com"]
    start_urls = ['http://www.ifeng.com/']
    id=0
    rules = (
        Rule(LinkExtractor(allow = (),restrict_xpaths = ('//a[contains(@href, "shtml")]')),
                           callback = 'parse_item',
                           follow = True),
    )

    def restart(self):
        with open(self.settings.get('CACHE_PATH')) as file:
            self.id = int(file.read())

    def parse_start_url(self, response):
        self.restart()
        item = IfengUrlspiderToMongodbItem()
        sel = Selector(response)
        url_list = sel.xpath('//a[contains(@href, "shtml")]').extract()
        pattern_url = re.compile(r"(?<=href=\").*?(?=\")")
        pattern_artical = re.compile(r'/a/')
        for url_item in url_list:
            href_list = re.findall(pattern_url, url_item)
            for href_item in href_list:
                requestedItem = re.findall(pattern_artical, href_item)
                if len(requestedItem) != 0:
                    self.id += 1
                    item['url'] = href_item.split('%')[0].strip('/').strip('?')
                    item['id'] = str(self.id)
                    yield item

    def parse_item(self, response):
        self.restart()
        item = IfengUrlspiderToMongodbItem()
        sel = Selector(response)
        not_fnd = sel.xpath(".//*[@class='tips404']").extract()
        if len(not_fnd) != 1:
            url_list = sel.xpath('//a[contains(@href, "shtml")]').extract()
            pattern_url = re.compile(r"(?<=href=\").*?(?=\")")
            pattern_artical = re.compile(r'/a/')
            for url_item in url_list:
                href_list = re.findall(pattern_url, url_item)
                for href_item in href_list:
                    requestedItem = re.findall(pattern_artical, href_item)
                    if len(requestedItem) != 0:
                        self.id += 1
                        item['url'] = href_item.split('%')[0].strip('/').strip('?')
                        item['id'] = str(self.id)
                        yield item