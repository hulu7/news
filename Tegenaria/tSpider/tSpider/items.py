# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IfengspiderToMongodbItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    comment_number = scrapy.Field()
    join_number = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    author_name = scrapy.Field()
    title = scrapy.Field()

class IfengspiderFromMongodbItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()

class HuspiderToMongodbItem(scrapy.Item):
    # define the fields for your item here like:
    comment_number = scrapy.Field()
    share_number = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    author_url = scrapy.Field()
    author_name = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()