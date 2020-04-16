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
        self.rootPath = '/home/dev/Data/Production/data4deepinews'
        self.path = '/home/dev/Data/Production/data4deepinews/{0}.csv'.format(self.today)
        self.logpath = '/home/dev/Data/Log/{0}_log.log'.format(self.today)

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

    def writeToTxtAdd(self, file_path, content):
        with open(file_path, 'a') as txt_writer:
            txt_writer.write(str(content) + '\n')
        txt_writer.close()

    def logger(self, file_path, content):
        local_time = time.localtime(time.time())
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        self.writeToTxtAdd(file_path, str(current_time + ": " + content))

    def updateData(self):
        if os.path.exists(self.rootPath) is False:
            os.makedirs(self.rootPath)
        tik = 120
        while tik > 0:
            tik -= 1
            time.sleep(1)
            try:
                currentUrl = ''
                if os.path.exists(self.path):
                    message1 = "file: {0} exits and start to update mongo.".format(self.path)
                    print message1
                    raw_data = self.readFromCSV(self.path)
                    data_length = len(raw_data)
                    if data_length < 2:
                        print "no mongo data to update."
                    else:
                        for i in range(1, data_length):
                            currentUrl = raw_data[i][1]
                            self.insert(self.formatData(raw_data[i]))
                            message2 = 'mongo {0} is updated.'.format(currentUrl)
                            print message2
                            self.logger(self.logpath, message2)
                        print "update done."
                    os.remove(self.path)
                    print "file: {0} delete done.".format(self.path)
                    print "waiting..."
            except Exception as e:
                message3 = "Exception: {0} to update mongo: {1}.".format(e.message, currentUrl)
                print message3
                self.logger(self.logpath, message3)

if __name__ == '__main__':
    u = UpdateMongoDeepNews()
    u.updateData()