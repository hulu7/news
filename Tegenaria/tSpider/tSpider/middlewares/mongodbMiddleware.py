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
from settings import Settings

class MongoMiddleware():
    def insert(self, database, data):
        client = pymongo.MongoClient(Settings.MONGO_URI, replicaset=Settings.REPLICASET)
        db = client[database]
        db.contentInfo.insert(data)
        client.close()
        del client, db
        gc.collect()
