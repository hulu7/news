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
from datetime import datetime
from datetime import timedelta
import redis
import hashlib
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.mongodbMiddleware import MongoMiddleware
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from bloomfilterOnRedis import BloomFilter

class Doraemon():

    def __init__(self):
        settings = Settings()
        settings.CreateCommonSettings()
        self.file = FileIOMiddleware()
        self.rconn = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)
        self.bf = BloomFilter(self.rconn, settings.BLOOMFILTER_NAME)
        self.disable_restart_interval = settings.DISABLE_RESTART_INTERVAL
        self.bf_weixin_url = BloomFilter(self.rconn, settings.FINISHED_WEIXIN_URL_ARTICLE)
        self.bf_weixin_content = BloomFilter(self.rconn, settings.FINISHED_WEIXIN_CONTENT_ARTICLE)
        self.bf_weixin_id = BloomFilter(self.rconn, settings.FINISHED_WEIXIN_URL_ID)
        self.md5 = hashlib.md5()

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
        isExceed = ((now - past) // 60 >= restart_interval) or (self.disable_restart_interval is True)
        if isExceed is True:
            self.file.writeToTxtCover(path, time.time())
        return isExceed

    def isEmpty(self, item_list):
        return len([item for item in item_list if item.strip()]) == 0

    def isDuplicated(self, filter, content):
        content_encode = str(content).encode("utf-8")
        if filter.isContains(content_encode):
            print 'Content {0} duplicated!'.format(content)
            return True
        else:
            filter.insert(content_encode)
            print 'Content {0} not duplicated!'.format(content)
            return False

    def isFinished(self, filter, content):
        content_encode = str(content).encode("utf-8")
        if filter.isContains(content_encode):
            print 'Content {0} exists!'.format(content)
            return True
        else:
            return False

    def storeFinished(self, filter, content):
        print 'Start to store content: {0}'.format(content)
        content_encode = str(content).encode("utf-8")
        filter.insert(content_encode)

    def storeMongodb(self, mongo_url, data):
        mongo = MongoMiddleware()
        mongo.insert(mongo_url, data)

    def storeTxt(self, id, content, finished_txt_path, name):
        self.createFilePath(finished_txt_path)
        print 'Start to store txt: {0}'.format(id)
        self.file.writeToTxtCover('{0}//{1}_{2}.txt'.format(finished_txt_path, name, id), content)
        print 'End to store txt: {0}'.format(id)

    def storeHtml(self, id, content, finished_html_path):
        self.createFilePath(finished_html_path)
        print 'Start to store html: {0}'.format(id)
        self.file.writeToHtmlCover('{0}//{1}.html'.format(finished_html_path, id), content)
        print 'End to store html: {0}'.format(id)

    def filter(self, filter, url_titles):
        new_url_titles = []
        for url_title in url_titles:
            if self.isFinished(filter, url_title[1]) is False:
                new_url_titles.append(url_title)
        return new_url_titles

    def readNewUrls(self, filter, url_path):
        print 'Start to read urls'
        isUrlPathExit = os.path.exists(url_path)
        new_url_titles = []
        if isUrlPathExit is True:
            url_titles = np.array(self.file.readColsFromCSV(url_path, ['url', 'title']))
            new_url_titles = self.filter(filter, url_titles)
        return new_url_titles

    def hashSet(self, name, key, value):
        self.rconn.hset(name, key, value)

    def getHashSet(self, name, key):
        return self.rconn.hget(name, key)

    def getAllHasSet(self, name):
        return self.rconn.hgetall(name)

    def delHashSet(self, name, key):
        return self.rconn.hdel(name, key)

    def delKey(self, key):
        return self.rconn.delete(key)

    def getKeyLen(self, key):
        return self.rconn.hlen(key)

    def getDateOfDaysBefore(self, days):
        return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    def getDataFromString(self, string_date):
        if "今天" in string_date:
            return self.getDateOfDaysBefore(0)
        if "昨天" in string_date:
            return self.getDateOfDaysBefore(1)
        if "前天" in string_date:
            return self.getDateOfDaysBefore(2)
        if "3天前" in string_date:
            return self.getDateOfDaysBefore(3)
        if "4天前" in string_date:
            return self.getDateOfDaysBefore(4)
        if "5天前" in string_date:
            return self.getDateOfDaysBefore(5)
        if "6天前" in string_date:
            return self.getDateOfDaysBefore(6)
        if "1周前" in string_date:
            return self.getDateOfDaysBefore(7)
        else:
            return string_date

    def getMD5(self, content):
        self.md5.update(content.encode('utf-8'))
        return self.md5.hexdigest()
