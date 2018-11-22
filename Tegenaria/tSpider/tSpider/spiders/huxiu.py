# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from tSpider.items import HuspiderToMongodbItem

class HuxiuSpider(CrawlSpider):
    name = 'huxiu'
    allowed_domains = ['huxiu.com']
    base_url = 'http://huxiu.com/article/'

    def start_requests(self):
        with open(self.settings.get('HUXIU_CACHE_PATH')) as file:
            restart = int(file.read()) + 1

        for page in range(restart, self.settings.get('MAX_PAGE')):
            url = self.base_url + str(page) + '.html'
            yield Request(url, callback=self.parse)


    def parse(self, response):
        not_fnd = response.xpath(".//*[@class='no-fnd-in']").extract()
        if len(not_fnd) != 1:
            article = response.xpath(".//*[@class='article-wrap']")

            comment_number = filter(str.isdigit,article.xpath(".//*[@class='article-pl pull-left']/text()").extract()[0].encode('gbk'))
            share_number = filter(str.isdigit,article.xpath(".//*[@class='article-share pull-left']/text()").extract()[0].encode('gbk'))
            image_url = article.xpath(".//*[@class='article-img-box']/img/@src").extract()[0]
            url = response.url
            content = article.xpath(".//div[@class='article-content-wrap']").xpath('string(.)').extract()[0].strip()
            time = article.xpath(".//*[@class='article-time pull-left']/text()").extract()[0]
            author_url = response.urljoin(article.xpath(".//*[@class='author-name']/a/@href").extract()[0])
            author_name = article.xpath(".//*[@class='author-name']/a/text()").extract()[0]
            title = article.xpath(".//*[@class='t-h1']/text()").extract()[0].strip()
            id = filter(str.isdigit, response.url)

            articleItem = HuspiderToMongodbItem(comment_number=comment_number,
                                                share_number=share_number,
                                                image_url=image_url,
                                                url=url,
                                                content=content,
                                                time=time,
                                                author_url=author_url,
                                                author_name=author_name,
                                                title=title,
                                                id=id)
            yield articleItem