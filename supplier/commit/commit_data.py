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
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
from bloomfilterOnRedis import BloomFilter
import redis

class CommitData():
    def __init__(self):
        self.rconn = redis.Redis('127.0.0.1', 6379)
        self.bf_huxiu = BloomFilter(self.rconn, 'supplier:commit_huxiu')
        self.today = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.class_finished_path = '/home/dev/Data/Production/catalogs'
        self.log_path = '/home/dev/Data/Production/log/{0}_log.log'.format(self.today)
        self.customer_info_path = '/home/dev/Data/Production/customerInfo/customers.xlsx'
        self.data4customers_path = '/home/dev/Data/Production/data4customers'
        self.model_huxiu_title_path = '/home/dev/Data/npl/classifier/fastText/model_data/news_fasttext.model.huxiu.bin'
        self.model_huxiu_content_path = '/home/dev/Data/npl/classifier/fastText/model_data/news_fasttext.model.huxiu_content.bin'
        self.classifier_content = fasttext.load_model(self.model_huxiu_content_path)
        self.classifier_title = fasttext.load_model(self.model_huxiu_title_path)
        self.since = time.time()

    def isDuplicated(self, title, filter):
        title_encode = str(title).encode("utf-8")
        if filter.isContains(title_encode):
            print 'Title {0} exists!'.format(title)
            return True
        else:
            filter.insert(title_encode)
            print 'Title {0} not exist!'.format(title)
            return False

    def storeFinished(self, title, filter):
        print 'Start to store title: {0}'.format(title)
        title_encode = title.encode("utf-8")
        filter.insert(title_encode)

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

    def isContentForRightCatalog(self, content, title):
        text = content.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
        texts = [" ".join(seg_text)]
        labels = self.classifier_content.predict_proba(texts, k=1)
        print "title: {0} -- {1}".format(title, labels)
        if labels[0][0][0] == u'__label__Y':
            return True
        else:
            return False

    def isTitleForRightCatalog(self, title):
        text = title.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
        texts = [" ".join(seg_text)]
        labels = self.classifier_title.predict_proba(texts, k=1)
        print "title: {0} -- {1}".format(title, labels)
        if labels[0][0][0] == u'__label__Y':
            return True
        else:
            return False


    def commitSingleCatalogSource(self, customer_id, catalog_name, source_name, customer_data_folder, customer_data_folder_txt):
        catalog_file_path = '{0}/{1}/{2}.csv'.format(self.class_finished_path, catalog_name, catalog_name)
        catalog_exists = os.path.exists(catalog_file_path)
        if catalog_exists is False:
            return
        commit_csv_path = '{0}/{1}.csv'.format(customer_data_folder, self.today)
        current_catalog_data = self.readFromCSV(catalog_file_path)
        today_int = int(self.today)
        commit_csv_exists = os.path.exists(commit_csv_path)
        if commit_csv_exists is False:
            self.writeToCSVWithoutHeader(commit_csv_path, ['id', 'title', 'url', 'time', 'catalog', 'deep', 'is_open_cache', 'source'])

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
                if self.isDuplicated(title, self.bf) is False:
                    file = '{0}_{1}.txt'.format(source_name, id)
                    origin_txt_path = '{0}/{1}/txt/{2}'.format(self.class_finished_path, catalog_name, file)
                    destination_txt_path = '{0}/{1}'.format(customer_data_folder_txt, file)
                    origin_txt_exists = os.path.exists(origin_txt_path)
                    if origin_txt_exists is False:
                        continue
                    content_txt = self.readFromTxt(origin_txt_path)
                    if len(content_txt) == 0:
                        continue
                    content = content_txt[0]
                    if customer_id == 'dn201949100':
                        if self.isDuplicated(title, self.bf_huxiu) is False and self.isContentForRightCatalog(content, title) is True and self.isTitleForRightCatalog(title) is True:
                            self.storeFinished(title, self.bf_huxiu)
                        else:
                            continue
                    self.writeToCSVWithoutHeader(commit_csv_path, data)
                    copyfile(origin_txt_path, destination_txt_path)
                    self.storeFinished(title, self.bf)
                    time_elapsed = time.time() - self.since
                    print '{0}_{1}_{2} complete in {3}m {4}s'.format(catalog_name, source_name, data[0], time_elapsed // 60, time_elapsed % 60)

    def startCommit(self):
        customers = self.readAllLinesFromExcel(self.customer_info_path, 'Sheet1')
        for customer in customers:
            customer_id = customer[0]
            customer_catalogs = customer[3].split(',')
            customer_sources = customer[4].split(',')
            customer_data_folder = '{0}/{1}/{2}'.format(self.data4customers_path, customer_id, self.today)
            customer_data_folder_txt = '{0}/{1}/{2}/txt'.format(self.data4customers_path, customer_id, self.today)
            customer_data_exists = os.path.exists(customer_data_folder)
            self.bf = BloomFilter(self.rconn, customer_id)
            if customer_data_exists is False:
                os.makedirs(customer_data_folder)
                os.makedirs(customer_data_folder_txt)
            for catalog in customer_catalogs:
                for source in customer_sources:
                    self.commitSingleCatalogSource(customer_id, catalog, source, customer_data_folder, customer_data_folder_txt)
        time_elapsed = time.time() - self.since
        self.writeToTxt(self.log_path, "{0}: commit done! in {1}m {2}s".format(str(self.getCurrntTime()), time_elapsed // 60, time_elapsed % 60))
        print 'commit done! in {0}m {1}s'.format(time_elapsed // 60, time_elapsed % 60)

if __name__ == "__main__":
    commit = CommitData()
    commit.writeToTxt(commit.log_path, "{0}: start commit...".format(str(commit.getCurrntTime())))
    print "start commit..."
    commit.startCommit()