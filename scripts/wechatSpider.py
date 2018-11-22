#coding=utf-8
import requests
import utils
import time
import codecs
from datetime import datetime
import csv
import re
import xlrd
import time
from shutil import copyfile
import pandas as pd
import wechatsogou
import csv
import re
import os
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WeChatSpider():
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

    def writeToTxt(self, filePath, content):
        with open(filePath, 'a+') as txt_file:
            txt_file.write(content)
            txt_file.write('\n')
        return txt_file.close()

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def readAllLinesFromExcel(self, file_path, sheet_name):
        sheets = xlrd.open_workbook(file_path)
        table = sheets.sheet_by_name(sheet_name)
        all_lines = []
        for row in range(0, table.nrows):
            all_lines.append(table.row_values(row))
        return all_lines

    def writeToMongo(self, content, id):
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019', replicaset='repset')
        db = client[id]
        mongodbItem = dict(content)
        db.contentInfo.insert(mongodbItem)
        client.close()

    def writeToCSVWithoutHeader(self, filePath, content):
        with open(filePath, 'a') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(content)
        csv_file.close()

    def getCurrntTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def parseData(self, id, history_list, finishedIdPath, saveFilePath):
        article_list = history_list['article']
        if len(article_list) == 0:
            return
        for article in article_list:
            finishedIds = self.readFromCSV(finishedIdPath)
            if [str(article['fileid'])] not in finishedIds:
                mongoItem = {
                    'title': article['title'],
                    'abstract': article['abstract'],
                    'author': article['author'],
                    'content_url': article['content_url'],
                    'copyright_stat': str(article['copyright_stat']),
                    'cover': article['cover'],
                    'datetime': str(article['datetime']),
                    'fileid': str(article['fileid']),
                    'main': str(article['main']),
                    'send_id': str(article['send_id']),
                    'source_url': article['source_url'],
                    'type': str(article['type'])
                }
                self.writeToMongo(mongoItem, id)
                self.writeToCSV(finishedIdPath, [str(article['fileid'])])
                finishedIds.append(str(article['fileid']))
                self.writeToCSVWithoutHeader(saveFilePath, [
                    article['title'],
                    article['abstract'],
                    article['author'],
                    article['content_url'],
                    str(article['copyright_stat']),
                    article['cover'],
                    str(article['datetime']),
                    str(article['fileid']),
                    str(article['main']),
                    str(article['send_id']),
                    article['source_url'],
                    str(article['type'])
                ])
                print article['title'] + '_' + article['abstract'] + '_' + article['author'] + '_' + article[
                    'content_url'] + '_' + \
                      str(article['copyright_stat']) + '_' + article['cover'] + '_' + str(
                    article['datetime']) + '_' + str(article['fileid']) + \
                      str(article['main']) + '_' + str(article['send_id']) + '_' + article['source_url'] + '_' + str(
                    article['type'])

    def startWeChatSpider(self, wechat_id_path, base_path, log_path):
        ws_api = wechatsogou.WechatSogouAPI()
        ids = self.readAllLinesFromExcel(wechat_id_path, 'gongzhonghao')
        for id in ids:
            finishedIdPath = base_path + '/' + id[0] + '_finished_id.csv'
            saveFilePath = base_path + '/' + id[0] + '_.csv'
            isFinishedIdFileExits = os.path.exists(finishedIdPath)
            isSaveFilePath = os.path.exists(saveFilePath)
            if isSaveFilePath is False:
                self.writeToCSV(saveFilePath, ['title',
                                                 'abstract',
                                                 'author',
                                                 'content_url',
                                                 'copyright_stat',
                                                 'cover' ,
                                                 'datetime',
                                                 'fileid',
                                                 'main',
                                                 'send_id',
                                                 'source_url',
                                                 'type'])
            if isFinishedIdFileExits is False:
                self.writeToCSV(finishedIdPath, ['finished_id'])
            history_list = ws_api.get_gzh_article_by_history(id[0])
            if len(history_list) > 0:
                self.parseData(id[0], history_list, finishedIdPath, saveFilePath)
            time.sleep(1)
        wechatSpider.writeToTxt(log_path, str(wechatSpider.getCurrntTime() + ": finished get gongzhonghao..."))

if __name__ == '__main__':
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_path = '/home/dev/Data/Production/log/' + today + '.log'
    wechat_id_path = '/home/dev/Data/Production/customerInfo/customers.xlsx'
    base_path = '/home/dev/Data/dev'
    wechatSpider = WeChatSpider()
    wechatSpider.writeToTxt(log_path, str(wechatSpider.getCurrntTime() + ": start get gongzhonghao..."))
    wechatSpider.startWeChatSpider(wechat_id_path, base_path, log_path)
