# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import jieba
import jieba.posseg as posseg
import pandas as pd
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MergeClass():
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

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def merge(self, classed_file_path, deep_file_path, fileout_path):
        classed_file_list = self.readFromCSV(classed_file_path)
        deep_file_list = self.readFromCSV(deep_file_path)
        deep_ids = list(self.readColsFromCSV(deep_file_path, ['id'])._get_values)

        for file in classed_file_list:
            id = re.findall(r"\d+\.?\d*", file[0].decode('utf-8'))
            if classed_file_list.index(file) == 0:
                isOutputFileExists = os.path.exists(fileout_path)
                if isOutputFileExists is False:
                    self.writeToCSVWithoutHeader(fileout_path, file + ['deep'])
                continue
            if [int(id[0])] in deep_ids:
                self.writeToCSVWithoutHeader(fileout_path, file + [str(deep_file_list[deep_ids.index([int(id[0])])][1])])
                print id[0] + '--' + str(deep_file_list[deep_ids.index([int(id[0])])])

if __name__ == "__main__":
    classed_file_path = '/home/dev/Data/rsyncData/prd1/ifeng/classes.csv'
    deep_file_path = '/home/dev/Repository/news/scripts/deep_ifeng.csv'
    fileout_path = '/home/dev/Data/rsyncData/prd1/ifeng/classes_deep.csv'
    merge = MergeClass()
    merge.merge(classed_file_path, deep_file_path, fileout_path)