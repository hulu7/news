# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfzmspiderToMongodbItem(scrapy.Item):
    # define the fields for your item here like:
    comment_number = scrapy.Field()
    share_sina_number = scrapy.Field()
    share_tencentweibo_number = scrapy.Field()
    share_qzone_number = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    author_name = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
