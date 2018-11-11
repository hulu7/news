#coding=utf-8
import requests
import utils
import time
import codecs
from datetime import datetime
import pandas as pd
import wechatsogou
import csv
import re
import os
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UrlCrawler():
    def crawl_pages(self):
        ws_api = wechatsogou.WechatSogouAPI()
        url_object_list = ws_api.get_gzh_article_by_history(self.id)
        if len(url_object_list) == 0:
            return
        for url_object in url_object_list:
            print url_object['i'] + '_' + url_object['j'] + '_' + self.restart['total'] + '_' + class_name
            self.writeToTxt(self.cacheFilePath, url_object['i'] + '_' + url_object['j'] + '_' + self.restart['total'] + '_' + self.topic)
            items = self.crawl_one_page(url_object, base_url)
            mongo
            if items != None:
                for item in items:
                    finishedIds = self.readFromCSV(self.finishedIdPath)
                    if [item['id']] not in finishedIds:
                        mongoItem = {
                            'catalog':self.topic,
                            'content':{
                            'collect_time':item['collect_time'],
                            'id':item['id'],
                            'title':item['title'],
                            'class':class_name,
                            'url':item['url'],
                            'docUrl':item['docUrl'],
                            'imageUrl':item['imageUrl'],
                            'i_j_total':self.restart['total']
                            }
                        }
                        self.writeToMongo(mongoItem)
                        self.writeToCSV(self.finishedIdPath, [item['id']])
                        self.restart['total'] = str(int(self.restart['total']) + 1)
                        self.writeToTxt(self.cacheFilePath, url_object['i'] + '_' + url_object['j'] + '_' + self.restart['total'] + '_' + self.topic)
                        print url_object['i'] + '_' + url_object['j'] + '_' + self.restart['total'] + '---' + item['docUrl'] + '---' + item['title'] + '---' + class_name

    def writeToCSV(self, file_path, content):
        with open(file_path, 'a') as scv_file:
            csv_writer = csv.writer(scv_file)
            csv_writer.writerow(content)
        scv_file.close()

    def readFromCSV(self, file_path):
        content = []
        with open(file_path, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def readFromTxt(self, file_path):
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
        txt_file.close()
        return content

    def writeToTxt(self, file_path, content):
        with open(file_path, 'w') as txt_writer:
            txt_writer.write(content)
        txt_writer.close()

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def readCacheInfo(self, file_path):
        restart = {}
        cache = re.split('_', self.readFromTxt(file_path).strip('\n'))
        restart['i'] = str(cache[0])
        restart['j'] = str(cache[1])
        restart['total'] = str(cache[2])
        restart['class'] = str(cache[3])
        return restart

    def writeToMongo(self, content):
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019', replicaset='repset')
        db = client['huxiu_wechat']
        mongodbItem = dict(content)
        db.contentInfo.insert(mongodbItem)
        client.close()

    def writeToCSVWithoutHeader(self, filePath, content):
        with open(filePath, 'a') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(content)
        csv_file.close()

    def startIfengUrlSpider(self, id, file_path):
        self.id = id
        self.finishedIdPath = file_path + '/files/huxiu/wechat/finished_id.csv'

        self.finishedIds = []

        isFinishedIdFileExits = os.path.exists(self.finishedIdPath)
        if isFinishedIdFileExits:
            self.finishedIds = self.readFromCSV(self.finishedIdPath)
        else:
            self.writeToCSV(self.finishedIdPath, ['finished'])

        self.crawl_pages()


if __name__ == '__main__':
    id = 'MissMoney浮世'
    basePath = '/home/dev/Data'
    urlSpider = UrlCrawler()
    urlSpider.startIfengUrlSpider(id, basePath)
