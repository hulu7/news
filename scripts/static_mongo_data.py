#coding:utf-8
#------requirement------
#pymongo-3.7.1
#------requirement------
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class StaticMongoData():
    def __init__(self):
        self.MONGO_URI = 'mongodb://127.0.0.1:27017'
        self.DATABASE = 'DeepNewsDatabase'

    def staticData(self):
        client = pymongo.MongoClient(self.MONGO_URI)
        db = client[self.DATABASE]
        count = db.articles.count({'subscribe': {'$in': ['dn201900001']}})
        print count
        client.close()

if __name__ == '__main__':
    u = StaticMongoData()
    u.staticData()