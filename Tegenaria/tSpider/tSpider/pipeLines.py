# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo
import csv
from items import IfengspiderToMongodbItem
from items import HuspiderToMongodbItem

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
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'ifeng_content'),
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

    def writeToCSV(self, file_path, content):
        with open(file_path, 'a') as scv_file:
            csv_writer = csv.writer(scv_file)
            csv_writer.writerow(content)
        scv_file.close()

    def _process_ifengspider_item(self, item, spider):
        file_name = spider.name + "_" + str(item['id']) + "_" + ".txt"
        fp = open(spider.settings.get('TXT_PATH') + '/' + file_name, 'w')
        fp.write(item['content'])
        fp.close()
        mongodbItem = dict(item)
        mongodbItem.pop('content')
        self.db.contentInfo.insert(mongodbItem)
        self.writeToCSV(spider.settings.get('FINISHED_PATH'), [item['id']])

class HuspiderToMongodbPipeline(object):
    def __init__(self, mongo_uri, mongo_db,replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'huxiu'),
            replicaset = crawler.settings.get('REPLICASET')
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri,replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,HuspiderToMongodbItem):
            self._process_huspider_item(item)
        return item

    def _process_huspider_item(self,item):
        mongodbItem = dict(item)
        mongodbItem.pop('content')
        self.db.contentInfo.insert(mongodbItem)

class HuspiderToTxtPipeline(object):
    def process_item(self, item, spider):
        file_name = spider.name + "_" + item['id'] + "_" + ".txt"
        fp = open(spider.settings.get('HUXIU_TXT_PATH') + '/' + file_name, 'w')
        fp.write(item['content'])
        fp.close()
        cache = open(spider.settings.get('HUXIU_CACHE_PATH'), 'w')
        cache.write(filter(str.isdigit, item['url']))
        cache.close()
        return item