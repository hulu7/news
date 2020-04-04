#coding:utf-8
#------requirement------
#pymongo-3.7.1
#------requirement------
import os
import pymongo
import sys
import csv
import time
from dateutil import parser
reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateMongoDeepNews():
    def __init__(self):
        self.MONGO_URI = 'mongodb://127.0.0.1:27017'
        self.DATABASE = 'DeepNewsDatabase'
        self.today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.path = '/home/dev/Data/Production/data4deepinews/{0}.csv'.format(self.today)

    def readFromCSV(self, filePath):
        content = []
        with open(filePath, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def insert(self, data):
        client = pymongo.MongoClient(self.MONGO_URI)
        db = client[self.DATABASE]
        db.articles.insert(data)
        client.close()

    def getUsers(self, data):
        users = data.split(',')
        users.append('admin')
        return users

    def cutTitle(self, title):
        decoded_title = title.decode('utf8')
        if len(decoded_title) > 36:
            short_title = "{0}...".format(decoded_title[0:35].encode('utf8'))
            return short_title
        else:
            return title

    def formatData(self, data):
        title = self.cutTitle(data[0])
        images = data[6].replace(']', '').replace('[', '').replace('"','').split(",")
        format_data = {
                   'title': title,
                   'isActive': 'true',
                   'recommend': [],
                   'columnID': '',
                   'columnName': 'article',
                   'author': data[5],
                   'clickVolume': '',
                   'forceUrl': data[1],
                   'articleCover': images,
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

    def updateData(self):
        while True:
            time.sleep(1)
            if os.path.exists(self.path):
                print "file: {0} exits and start to update mongo.".format(self.path)
                raw_data = self.readFromCSV(self.path)
                data_length = len(raw_data)
                for i in range(1, data_length):
                    self.insert(self.formatData(raw_data[i]))
                    print 'data {0} is updated.'.format(raw_data[i][1])
                if data_length < 2:
                    print "no data to update.".format(self.path)
                else:
                    print "update done.".format(self.path)
                os.remove(self.path)
                print "file: {0} delete done.".format(self.path)
                print "waiting..."

if __name__ == '__main__':
    u = UpdateMongoDeepNews()
    u.updateData()