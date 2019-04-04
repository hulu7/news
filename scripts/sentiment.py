# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import pandas as pd
import os
import sys
import shutil
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from bloomfilterOnRedis import BloomFilter
import redis
import xmnlp

class Sentiment():
    def __init__(self):
        self.rconn = redis.Redis('127.0.0.1', 6379)
        self.bf = BloomFilter(self.rconn, 'supplier:merge')

    def isDuplicated(self, title):
        title_encode = str(title).encode("utf-8")
        if self.bf.isContains(title_encode):
            print 'Title {0} exists!'.format(title)
            return True
        else:
            self.bf.insert(title_encode)
            print 'Title {0} not exist!'.format(title)
            return False

    def storeFinished(self, title):
        print 'Start to store title: {0}'.format(title)
        title_encode = title.encode("utf-8")
        self.bf.insert(title_encode)

    def readFromCSV(self, filePath):
        content = []
        with open(filePath, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def writeToCSVWithHeader(self, filePath, content, header):
        with open(filePath, 'a') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            if len(content) > 0 and type(content) == type(content[0]):
                for item in content:
                    csv_writer.writerow(item)
            else:
                csv_writer.writerow(content)
        csv_file.close()

    def writeToCSVWithoutHeader(self, filePath, content):
        with open(filePath, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(content)
        csv_file.close()

    def readFromTxt(self, file_path):
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
            split_list = re.split('\n', content)
        txt_file.close()
        return list(filter(None, split_list))

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols


    def analysis(self, filein_path, fileout_path):
        isFileInExists = os.path.exists(filein_path)
        isFileOutExists = os.path.exists(fileout_path)
        if isFileInExists is False:
            print 'in file: {0} not exits.'.format(filein_path)
            return
        if isFileOutExists is False:
            print 'out file: {0} not exits.'.format(fileout_path)
            self.writeToCSVWithoutHeader(fileout_path,['share_number', 'comment_number', 'url', 'title', 'sentiment'])
            print 'create an new out file: {0}.'.format(fileout_path)

        in_content = self.readFromCSV(filein_path)
        in_content.pop(0)
        for item in in_content:
            s = xmnlp.sentiment(item[3])
            self.writeToCSVWithoutHeader(fileout_path,[item[0], item[1], item[2], item[3], s])
            print "{0}--{1}".format(item[3], s)

if __name__ == "__main__":
    filein = '/home/dev/Data/test/huxiu_backup.csv'
    fileout = '/home/dev/Data/test/output.csv'
    sentiment = Sentiment()
    sentiment.analysis(filein, fileout)