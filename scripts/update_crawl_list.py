#coding=utf-8
import requests
import utils
import time
from datetime import datetime
import csv
import re
import os
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd

class UpdateCrawlList():
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
    def readColFromCSV(self, file_path, col_name):
        with open(file_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            col = [row[col_name] for row in reader]
        csvfile.close()
        return col

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def updateFinishedList(self, file_path, site_name):
        self.finishedIdPath = file_path + 'prd1/' + site_name + '/finished_id.csv'
        self.globalFinishedIdPath = file_path + 'prd2/' + site_name + '/global_finished_id.csv'
        isFinishedIdFileExits = os.path.exists(self.finishedIdPath)
        if isFinishedIdFileExits:
            self.finishedIds = self.readFromCSV(self.finishedIdPath)
        else:
            self.finishedIds=[]
        isGlobalFinishedIdFileExits = os.path.exists(self.globalFinishedIdPath)
        if isGlobalFinishedIdFileExits:
            self.globalFinishedIds = self.readFromCSV(self.globalFinishedIdPath)
            for finishedId in self.finishedIds:
                if finishedId in self.globalFinishedIds:
                    continue
                else:
                    self.globalFinishedIds.append(finishedId)
                    self.writeToCSV(self.globalFinishedIdPath, [finishedId])
        else:
            self.writeToCSV(self.globalFinishedIdPath, ['finished_ids'])
            self.globalFinishedIds = self.finishedIds
            for finishedId in self.finishedIds:
                self.writeToCSV(self.globalFinishedIdPath, finishedId)

        self.prepareNewList(site_name, file_path)

    def prepareNewList(self, site_name, file_path):
        self.newIdPath = file_path + 'prd2/' + site_name + '/new_id.csv'
        self.allIdPath = file_path + 'prd2/' + site_name + '/ifeng_urls.csv'
        isAllIdFileExists = os.path.exists(self.allIdPath)
        if isAllIdFileExists:
           self.allIdUrls = list(self.readColsFromCSV(self.allIdPath, ['content.id', 'content.docUrl'])._get_values)
        else:
            self.allIdUrls = []
        isNewIdFileExits = os.path.exists(self.newIdPath)
        if isNewIdFileExits:
            os.remove(self.newIdPath)
            for item in self.allIdUrls:
                if item[0] in self.globalFinishedIds:
                    continue
                else:
                    if str(item[0]).find(site_name) >= 0:
                        self.writeToCSV(self.newIdPath, [item[0], item[1]])
                    else:
                        continue
        else:
            for item in self.allIdUrls:
                if str(item[0]).find(site_name) >=0:
                    self.writeToCSV(self.newIdPath, [item[0], item[1]])
                else:
                    continue

if __name__ == "__main__":
    update = UpdateCrawlList()
    update.updateFinishedList('/home/dev/rsyncData/', 'ifeng')