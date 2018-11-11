# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import datetime
import codecs
import csv
import os
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd


class MergeCSV():
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
            csv_file.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(content)
        csv_file.close()

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def Merge(self, fileInPath, fileOutPath,  header):
        in_items = self.readFromCSV(fileInPath)
        isOutFileExists = os.path.exists(fileOutPath)
        if isOutFileExists is False:
            self.writeToCSVWithoutHeader(fileOutPath, header)
        out_items = list(self.readColsFromCSV(fileOutPath, ['id'])._get_values)
        for item in in_items:
            if in_items.index(item) == 0:
                continue
            if [int(item[1])] in out_items:
                continue
            else:
                self.writeToCSVWithoutHeader(fileOutPath, item)
                out_items.append([int(item[1])])

if __name__ == '__main__':
    print "starting..."
    since = time.time()
    merge = MergeCSV()
    mergeHeader = ['collect_time', 'id', 'title', 'class', 'url', 'docUrl', 'imageUrl', 'i_j_total']
    items=['军事', '体育', '娱乐', '新闻', '财经']
    fileOut = '/home/dev/Repository_Test_Data/ifeng/ifeng.csv'
    for item in items:
        fileIn = '/home/dev/Backups/prd1/files/ifeng/' + item + '.csv'
        merge.Merge(fileIn, fileOut, mergeHeader)
    time_elapsed = time.time() - since
    print('complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
