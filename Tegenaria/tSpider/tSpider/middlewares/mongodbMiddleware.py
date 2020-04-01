#coding:utf-8
#------requirement------
#pymongo-3.7.1
#------requirement------
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import gc
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from Tegenaria.tSpider.tSpider.settings import Settings

class MongoMiddleware():
    def __init__(self):
        self.settings = Settings()
        self.settings.CreateCommonSettings()

    def insert(self, database, data):
        client = pymongo.MongoClient(self.settings.MONGO_URI)
        db = client[self.settings.SPIDERDB]
        db[database].insert(data)
        client.close()
        del client, db
        gc.collect()
