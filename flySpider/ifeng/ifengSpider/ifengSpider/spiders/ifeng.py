# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from ifengSpider.items import IfengspiderToMongodbItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re

class IfengSpider(CrawlSpider):
    name = 'ifeng'
    allowed_domains = ["ifeng.com"]
    url_content_list = ['http://www.ifeng.com/']

    # rules = (
    #     Rule(LinkExtractor(allow = (),restrict_xpaths = ('//a[contains(@href, "shtml")]')),
    #                        callback = 'parse_item',
    #                        follow = True),
    # )

    def extract_url(self, response):
        sel = Selector(response)
        url_list = sel.xpath('//a[contains(@href, "shtml")]').extract()
        pattern_url = re.compile(r"(?<=href=\").*?(?=\")")
        pattern_artical = re.compile(r'/a/')
        for url_item in url_list:
            href_list = re.findall(pattern_url, url_item)
            for href_item in href_list:
                requestedItem = re.findall(pattern_artical, href_item)
                if len(requestedItem) != 0:
                    self.url_content_list.append(href_item.split('%')[0].strip('/'))

    def start_requests(self):
        for url in self.url_content_list:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        self.extract_url(response)
        not_fnd = response.xpath(".//*[@class='tips404']").extract()
        if len(not_fnd) != 1:
            article_j = response.xpath(".//*[@id='artical']")
            if len(article_j.extract()) > 0:
                article = article_j
                comment_number = filter(str.isdigit,article.xpath(".//*[@class='js_cmtNum']/text()").extract()[0].encode('gbk'))
                join_number = filter(str.isdigit,article.xpath(".//*[@class='js_joinNum']/text()").extract()[0].encode('gbk'))
                url = response.url
                content = article.xpath(".//div[@id='main_content']").xpath('string(.)').extract()[0].strip()
                time = article.xpath(".//*[@class='p_time']/text()").extract()[0]
                author_url = article.xpath(".//*[@itemprop='publisher']/a/@href").extract()[0]
                author_name = article.xpath(".//*[@itemprop='publisher']/a/text()").extract()[0]
                title = article.xpath(".//*[@id='artical_topic']/text()").extract()[0].strip()
                id = filter(str.isdigit, response.url)

                articleItem = IfengspiderToMongodbItem(
                                                    comment_number=comment_number,
                                                    join_number=join_number,
                                                    image_url=image_url,
                                                    url=url,
                                                    content=content,
                                                    time=time,
                                                    author_url=author_url,
                                                    author_name=author_name,
                                                    title=title,
                                                    id=id
                                                    )
                yield articleItem
