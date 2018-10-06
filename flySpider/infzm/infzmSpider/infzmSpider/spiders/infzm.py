# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from infzmSpider.items import InfzmspiderToMongodbItem

class InfzmSpider(CrawlSpider):
    name = 'infzm'
    allowed_domains = ['infzm.com']
    base_url = 'http://infzm.com/content/'

    def start_requests(self):
        with open(self.settings.get('CACHE_PATH')) as file:
            restart = int(file.read()) + 1

        for page in range(restart, self.settings.get('MAX_PAGE')):
            url = self.base_url + str(page)
            yield Request(url, callback=self.parse)


    def parse(self, response):
        not_fnd = response.xpath(".//*[@id='box']").extract()
        auth_lmt = response.xpath(".//*[@class='infzm-payment-limit']/text()").extract()
        if len(not_fnd) != 1 and len(auth_lmt) != 1:
            article = response.xpath(".//*[@id='mainContent']")
            comment_number = filter(str.isdigit,article.xpath(".//*[@class='toComment']/span/text()").extract()[0].encode('gbk'))
            share_sina_number = filter(str.isdigit,article.xpath(".//*[@id='share_count_sina']/text()").extract()[0].encode('gbk'))
            share_tencentweibo_number = filter(str.isdigit,article.xpath(".//*[@id='share_count_qqweibo']/text()").extract()[0].encode('gbk'))
            share_qzone_number = filter(str.isdigit,article.xpath(".//*[@id='share_count_qzone']/text()").extract()[0].encode('gbk'))

            url = response.url
            content = article.xpath(".//*[@id='articleContent']").xpath('string(.)').extract()[0].strip()
            time = article.xpath(".//*[@class='pubTime']/text()").extract()[0].strip()
            author_name = article.xpath(".//*[@id='content_author']/text()").extract()[0]
            title = article.xpath(".//*[@class='articleHeadline clearfix']/text()").extract()[0].strip()
            id = filter(str.isdigit, response.url)

            articleItem = InfzmspiderToMongodbItem(comment_number=comment_number,
                                                   share_sina_number=share_sina_number,
                                                   share_tencentweibo_number=share_tencentweibo_number,
                                                   share_qzone_number=share_qzone_number,
                                                   url=url,
                                                   content=content,
                                                   time=time,
                                                   author_name=author_name,
                                                   title=title,
                                                   id=id)
            yield articleItem