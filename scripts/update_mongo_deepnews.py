#coding:utf-8
#------requirement------
#pymongo-3.7.1
#------requirement------
import pymongo
import sys
import csv
import time
from dateutil import parser
reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateMongoDeepNews():
    def init(self):
        self.MONGO_URI = 'mongodb://127.0.0.1:27017'
        self.DATABASE = 'DeepNewsDatabase'

    def readFromCSV(self, filePath):
        content = []
        with open(filePath, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def insert(self, data):
        self.init()
        client = pymongo.MongoClient(self.MONGO_URI)
        db = client[self.DATABASE]
        db.articles.insert(data)
        client.close()

    def getUsers(self, data):

        users = data.split(',')

        users.append('admin')

        return users

    def formatData(self, data):
        format_data = {
                   'title': data[0],
                   'isActive': 'true',
                   'recommend': [],
                   'columnID': '',
                   'columnName': 'article',
                   'author': '',
                   'clickVolume': '',
                   'forceUrl': data[1],
                   'articleCover': 'images/image.jpg',
                   'published': parser.parse(data[2]),
                   'articleBrief': '',
                   'articleContent': '',
                   'pagetitle': '',
                   'pagekeywords': '',
                   'pagedescription': '',
                   'language': 'ch',
                   'comments': [],
                   'mark': [],
                   'catalog': [data[3]],
                   'subscribe': self.getUsers(data[4]),
                   'add': [],
                   'trash': []
                }

        return format_data

    def updateData(self, path):
        raw_data = self.readFromCSV(path)
        for i in range(1, len(raw_data)):
            self.insert(self.formatData(raw_data[i]))

if __name__ == '__main__':
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    u = UpdateMongoDeepNews()
    path = '/home/dev/Data/Production/data4deepinews/{0}.csv'.format(today)
    u.updateData(path)