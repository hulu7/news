# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import jieba
import jieba.posseg as posseg
import os
import sys
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

    def Filter(self, filein_path, fileout_path, keysfilter_path, dupfilter_path):
        content_list = self.readFromCSV(filein_path)
        filterkeys = self.readFromTxt(keysfilter_path)
        isDupFileExists = os.path.exists(dupfilter_path)
        if isDupFileExists is True:
            dupkeys = self.readFromCSV(dupfilter_path)
        else:
            dupkeys = []
            self.writeToCSVWithHeader(dupfilter_path, dupkeys, ['id'])
        for content in content_list:
            haskeys = False
            hasEmpty = False
            for item in content:
                if len(item) == 0:
                    hasEmpty = True
                    continue
            if content[4] in dupkeys:
                continue
            if content_list.index(content) == 0:
                continue
            for key in filterkeys:
                if key in content[6]:
                    haskeys = True
                    continue
            if haskeys == False and hasEmpty == False:
                out_items = content
                out_header = ['catalog', 'classes', 'time', 'docUrl', 'id', 'imageUrl', 'title', 'url']
                dup_items = [content[4]]
                isOutputFileExists = os.path.exists(fileout_path)
                if isOutputFileExists is True:
                    self.writeToCSVWithoutHeader(fileout_path, out_items)
                else:
                    self.writeToCSVWithHeader(fileout_path, out_items, out_header)
                self.writeToCSVWithoutHeader(dupfilter_path, dup_items)
            dupkeys = self.readFromCSV(dupfilter_path)

if __name__ == "__main__":
    filein = '/home/dev/rsyncData/prd2/ifeng/ifeng_urls.csv'
    fileout = '/home/dev/Production/class/file_after_filter.csv'
    keyfilter = '/home/dev/Production/class/filterkeys/keys.txt'
    dupfilter = '/home/dev/Production/class/filterdup/dup.csv'
    flt = ProductionFilter()
    flt.Filter(filein, fileout, keyfilter, dupfilter)