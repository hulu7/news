# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
from ifengSpider.items import IfengspiderToMongodbItem

class IfengspiderToTxtPipeline(object):
    def process_item(self, item, spider):
        file_name = spider.name + "_" + str(item['id']) + "_" + ".txt"
        fp = open(spider.settings.get('TXT_PATH') + '/' + file_name, 'w')
        fp.write(str(item['content']))
        fp.close()
        return item

class IfengspiderToMongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db,replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'ifeng'),
            replicaset = crawler.settings.get('REPLICASET')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, IfengspiderToMongodbItem):
            self._process_ifengspider_item(item, spider)
        return item

    def _process_ifengspider_item(self, item, spider):
        mongodbItem = dict(item)
        mongodbItem.pop('content')
        self.db.contentInfo.insert(mongodbItem)

        id_cache = open(spider.settings.get('CACHE_PATH'), 'w')
        next_id = int(item['id'])
        id_cache.write(str(next_id))
        id_cache.close()
