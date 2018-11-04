# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from ifengSpider.items import IfengspiderToMongodbItem, IfengspiderFromMongodbItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import csv
import pymongo

class IfengSpider(CrawlSpider):
    name = 'ifeng'
    allowed_domains = ["ifeng.com"]
    file_path = '/home/dev/rsyncData/prd2/ifeng/new_id.csv'

    def readFromCSV(self):
        content = []
        with open(self.file_path, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def start_requests(self):
        url_list = self.readFromCSV()
        for url_item in url_list:
            yield Request(url_item[0], meta={'id': url_item[1]}, callback=self.parse)

    def parse(self, response):
        url_id = int(response.meta['id'])
        sel = Selector(response)
        not_fnd = sel.xpath(".//*[@class='tips404']").extract()
        if len(not_fnd) != 1:
            article_0 = response.xpath(".//*[@id='artical']")
            article_1 = response.xpath(".//*[@class='yc_main wrap']")
            if len(article_0.extract()) > 0:
                article = article_0
                comment_number = filter(str.isdigit,article.xpath(".//*[@class='js_cmtNum']").xpath('string(.)').extract()[0].encode('gbk'))
                join_number = filter(str.isdigit,article.xpath(".//*[@class='js_joinNum']").xpath('string(.)').extract()[0].encode('gbk'))
                url = response.url
                content = article.xpath(".//div[@id='main_content']").xpath('string(.)').extract()[0].strip()
                time = article.xpath(".//*[@class='ss01']").xpath('string(.)').extract()[0].strip()
                author_name = article.xpath(".//*[@class='ss03']").xpath('string(.)').extract()[0]
                title = article.xpath(".//*[@id='artical_topic']").xpath('string(.)').extract()[0].strip()
                id = url_id
                articleItem = IfengspiderToMongodbItem(
                                                    comment_number=comment_number,
                                                    join_number=join_number,
                                                    url=url,
                                                    content=content,
                                                    time=time,
                                                    author_name=author_name,
                                                    title=title,
                                                    id=id
                                                    )
                yield articleItem
            if len(article_1.extract()) > 0:
                article = article_1
                comment_number = filter(str.isdigit,article.xpath(".//*[@class='js_cmtNum']").xpath('string(.)').extract()[0].encode('gbk'))
                join_number = filter(str.isdigit,article.xpath(".//*[@class='js_joinNum']").xpath('string(.)').extract()[0].encode('gbk'))
                url = response.url
                content = article.xpath(".//div[@id='yc_con_txt']").xpath('string(.)').extract()[0].strip()
                time = article.xpath(".//*[@class='yc_tit']//p//span").xpath('string(.)').extract()[0].strip()
                author_name = article.xpath(".//*[@class='yc_tit']//p//a").xpath('string(.)').extract()[0].strip()
                title = article.xpath(".//*[@class='yc_tit']//h1").xpath('string(.)').extract()[0].strip()
                id = url_id
                articleItem = IfengspiderToMongodbItem(
                                                    comment_number=comment_number,
                                                    join_number=join_number,
                                                    url=url,
                                                    content=content,
                                                    time=time,
                                                    author_name=author_name,
                                                    title=title,
                                                    id=id
                                                    )
                yield articleItem