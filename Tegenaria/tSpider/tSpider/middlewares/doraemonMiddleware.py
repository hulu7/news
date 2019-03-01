#coding:utf-8
#------requirement------
#redis-2.10.6
#------requirement------
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import numpy as np
import time
import redis
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from bloomfilterOnRedis import BloomFilter

class Doraemon():

    def __init__(self):

        self.file = FileIOMiddleware()
        self.rconn = redis.Redis(Settings.REDIS_HOST, Settings.REDIS_PORT)
        self.bf = BloomFilter(self.rconn, Settings.BLOOMFILTER_NAME)

    def createFilePath(self, path):
        isFilePathExists = os.path.exists(path)
        if isFilePathExists is False:
            os.makedirs(path)

    def isExceedRestartInterval(self, path, restart_interval):
        isRestartPathExists = os.path.exists(path)
        if isRestartPathExists is False:
            self.file.writeToTxtCover(path, time.time())
            return True
        past = float(self.file.readFromTxt(path))
        now = time.time()
        isExceed = (now - past) // 60 >= restart_interval
        if isExceed is True:
            self.file.writeToTxtCover(path, time.time())
        return isExceed

    def isEmpty(self, item_list):
        return len([item for item in item_list if item.strip()]) == 0

    def isDuplicated(self, title):
        title_encode = str(title).encode("utf-8")
        if self.bf.isContains(title_encode):
            print 'Title {0} exists!'.format(title)
            return True
        else:
            self.bf.insert(title_encode)
            print 'Title {0} not exist!'.format(title)
            return False

    def isFinished(self, title):
        title_encode = str(title).encode("utf-8")
        if self.bf.isContains(title_encode):
            print 'Title {0} exists!'.format(title)
            return True
        else:
            return False

    def storeFinished(self, title):
        print 'Start to store title: {0}'.format(title)
        title_encode = title.encode("utf-8")
        self.bf.insert(title_encode)

    def storeMongodb(self, mongo_url, data):
        mongo = MongoMiddleware()
        mongo.insert(mongo_url, data)

    def storeTxt(self, id, content, finished_txt_path, name):
        print 'Start to store txt: {0}'.format(id)
        self.file.writeToTxtCover('{0}//{1}_{2}.txt'.format(finished_txt_path, name, id), content)
        print 'End to store txt: {0}'.format(id)

    def filter(self, url_titles):
        new_url_titles = []
        for url_title in url_titles:
            if self.isFinished(url_title[1]) is False:
                new_url_titles.append(url_title)
        return new_url_titles

    def readNewUrls(self, url_path):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(url_path)
        new_url_titles = []
        if isUrlPathExit is True:
            url_titles = np.array(self.file.readColsFromCSV(url_path, ['url', 'title']))
            new_url_titles = self.filter(url_titles)
        return new_url_titles

    def hashSet(self, name, key, value):
        self.rconn.hset(name, key, value)

    def getHashSet(self, name, key):
        return self.rconn.hget(name, key)
