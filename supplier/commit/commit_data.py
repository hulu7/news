# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import xlrd
import time
from shutil import copyfile
import pandas as pd
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bloomfilterOnRedis import BloomFilter
import redis

class CommitData():
    def __init__(self):
        self.rconn = redis.Redis('127.0.0.1', 6379)
        self.bf = BloomFilter(self.rconn, 'supplier:commit')

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

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def writeToCSVWithHeader(self, filePath, content, header):
        with open(filePath, 'a') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            if type(content) == type(content[0]):
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

    def readFromTxt(self, file_path):
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
            split_list = re.split('\n', content)
        txt_file.close()
        return list(filter(None, split_list))

    def writeToTxt(self, filePath, content):
        with open(filePath, 'a+') as txt_file:
            txt_file.write(content)
            txt_file.write('\n')
        return txt_file.close()

    def extractTime(self, content):
        toGBK = content.encode('gbk')
        getDigit = filter(str.isdigit, toGBK)
        getYMD = getDigit[0:8]
        return getYMD

    def readOneLineFromExcel(self, file_path, sheet_name, line):
        sheets = xlrd.open_workbook(file_path)
        table = sheets.sheet_by_name(sheet_name)
        return table.row_values(line)

    def readAllLinesFromExcel(self, file_path, sheet_name):
        sheets = xlrd.open_workbook(file_path)
        table = sheets.sheet_by_name(sheet_name)
        all_lines = []
        for row in range(1, table.nrows):
            all_lines.append(table.row_values(row))
        return all_lines

    def getCurrntTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def commitSingleCatalogSource(self, catalog_name, source_name, customer_data_folder, customer_data_folder_txt):
        catalog_file_path = self.class_finished_path + '/' + catalog_name + '/' + catalog_name + '.csv'
        catalog_exists = os.path.exists(catalog_file_path)
        if catalog_exists is False:
            return
        commit_csv_path = customer_data_folder + '/' + self.today + '.csv'
        commit_finished_file_path = customer_data_folder + '/' + source_name + '_committed.csv'
        current_catalog_data = self.readFromCSV(catalog_file_path)
        today_int = int(self.today)
        commit_csv_exists = os.path.exists(commit_csv_path)
        commit_finished_exists = os.path.exists(commit_finished_file_path)
        if commit_csv_exists is False:
            self.writeToCSVWithoutHeader(commit_csv_path, ['id', 'title', 'url', 'time', 'catalog', 'deep', 'is_open_cache', 'source'])
        if commit_finished_exists is False:
            self.writeToCSVWithoutHeader(commit_finished_file_path, ['id'])

        finishedIds = []
        finished_list = self.readFromCSV(commit_finished_file_path)
        for finished_item in finished_list[1:]:
            finishedIds.append(str(finished_item[0].replace('\xef\xbb\xbf', '')))
        for data in current_catalog_data:
            if current_catalog_data.index(data) == 0:
                continue
            if source_name != data[8]:
                continue
            if len(data[3]) == 0:
                continue

            item_date_int = int(data[3])
            if item_date_int >= today_int:
                id = data[0].replace('\xef\xbb\xbf','')
                title = data[1]
                if self.isDuplicated(title) is False:
                    file = (source_name + '_' + id + '.txt')
                    origin_txt_path = self.class_finished_path + '/' + catalog_name + '/txt/' + file
                    destination_txt_path = customer_data_folder_txt + '/' + file
                    origin_txt_exists = os.path.exists(origin_txt_path)
                    if origin_txt_exists is False:
                        continue
                    self.writeToCSVWithoutHeader(commit_finished_file_path, [id])
                    self.writeToCSVWithoutHeader(commit_csv_path, data)
                    copyfile(origin_txt_path, destination_txt_path)
                    self.storeFinished(title)
                    finishedIds.append(id)
                    time_elapsed = time.time() - since
                    print(catalog_name + '_' + source_name + '_' + data[0] + ' and ' + str(len(finishedIds)) + 'itemts complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

    def startCommit(self, class_finished_path, customer_info_path, data4customers_path, log_path, today):
        self.class_finished_path = class_finished_path
        self.customer_info_path = customer_info_path
        self.data4customers_path = data4customers_path
        self.log_path = log_path
        self.today = today

        customers = self.readAllLinesFromExcel(customer_info_path, 'Sheet1')
        for customer in customers:
            customer_id = customer[0]
            customer_catalogs = customer[3].split(',')
            customer_sources = customer[4].split(',')
            customer_data_folder = self.data4customers_path + '/' + customer_id + '/' + self.today
            customer_data_folder_txt = self.data4customers_path + '/' + customer_id + '/' + self.today + '/txt'
            customer_data_exists = os.path.exists(customer_data_folder)
            if customer_data_exists is False:
                os.makedirs(customer_data_folder)
                os.makedirs(customer_data_folder_txt)
            for catalog in customer_catalogs:
                for source in customer_sources:
                    self.commitSingleCatalogSource(catalog, source, customer_data_folder, customer_data_folder_txt)
        time_elapsed = time.time() - since
        self.writeToTxt(log_path, str(commit.getCurrntTime() + ": " + 'commit done! in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60)))
        print 'commit done! in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60)

if __name__ == "__main__":
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    class_finished_path = '/home/dev/Data/Production/catalogs'
    log_path = '/home/dev/Data/Production/log/' + today + '.log'
    customer_info_path = '/home/dev/Data/Production/customerInfo/customers.xlsx'
    data4customers_path = '/home/dev/Data/Production/data4customers'

    since = time.time()
    commit = CommitData()
    commit.writeToTxt(log_path, str(commit.getCurrntTime() + ": start commit..."))
    print "start commit..."
    commit.startCommit(class_finished_path, customer_info_path, data4customers_path, log_path, today)