# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import pandas as pd
import os
import sys
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')

class ProductionFilter():
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

    def readFromTxt(self, file_path):
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
            split_list = re.split('\n', content)
        txt_file.close()
        return list(filter(None, split_list))

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def Filter(self, filein_path, fileout_path):
        files = os.listdir(filein_path)
        for file in files:
            in_csv_file = "{0}/{1}/{2}.csv".format(filein_path, file, file)
            in_txt_path = "{0}{1}/txt".format(filein_path, file)

            csv_content = self.readFromCSV(in_csv_file)
            finished_titles = []

            if len(csv_content) < 2:
                continue

            out_csv_file = "{0}/{1}/{2}.csv".format(fileout_path, file, file)
            out_txt_path = "{0}{1}/txt/".format(fileout_path, file)
            txt_list = os.listdir(in_txt_path)

            isOutputPathExists = os.path.exists(out_txt_path)
            if isOutputPathExists is False:
                os.makedirs(out_txt_path)
            isOutputFileExists = os.path.exists(out_csv_file)
            if isOutputFileExists is False:
                self.writeToCSVWithoutHeader(out_csv_file, csv_content[0])
            for item in csv_content[1:]:
                if item[1] in finished_titles:
                    continue
                if item[5] == '':
                    continue
                deep = int(item[5])
                if deep < 100:
                    continue
                id = item[0].replace('\xef\xbb\xbf', '')
                txt_name = ''
                for txt in txt_list:
                    if id in txt:
                        txt_name = txt
                        break
                new_txt_name = "{0}_{1}".format(item[1].replace('/',''), txt_name)
                in_txt_file = "{0}{1}/txt/{2}".format(filein_path, file, txt_name)
                out_txt_file = "{0}{1}".format(out_txt_path, new_txt_name)
                self.writeToCSVWithoutHeader(out_csv_file, item)
                shutil.copyfile(in_txt_file, out_txt_file)
                finished_titles.append(item[1])

if __name__ == "__main__":
    filein = '/home/dev/Data/tmp/catalogs/'
    fileout = '/home/dev/Data/tmp/result/'
    flt = ProductionFilter()
    flt.Filter(filein, fileout)