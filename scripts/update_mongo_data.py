#coding:utf-8
#------requirement------
#pymongo-3.7.1
#------requirement------
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateMongoData():
    def __init__(self):
        self.MONGO_URI = 'mongodb://127.0.0.1:27017'
        self.DATABASE = 'DeepNewsDatabase'

    def updateSingle(self, db, item):
        db.articles.update({"_id": item['_id']}, {'$addToSet':{'subscribe': 'dn201900001'}})

    def updateData(self):
        client = pymongo.MongoClient(self.MONGO_URI)
        db = client[self.DATABASE]
        items = db.articles.find({'subscribe': {'$in': ['dn201949100']}})
        for item in items:
            self.updateSingle(db, item)
        client.close()

if __name__ == '__main__':
    u = UpdateMongoData()
    u.updateData()