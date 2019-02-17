#coding:utf-8
#------requirement------
#redis-2.10.6
#------requirement------
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
import urlparse
import re
import time
import redis
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from browserRequest import BrowserRequest
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
        title_encode = title.encode("utf-8")
        if self.bf.isContains(title_encode):
            print 'Title {0} exists!'.format(title)
            return True
        else:
            self.bf.insert(title_encode)
            print 'Title {0} not exist!'.format(title)
            return False

    def storeMongodb(self, mongo_url, data):
        mongo = MongoMiddleware()
        mongo.insert(mongo_url, data)
