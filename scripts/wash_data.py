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

class WashData():
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

    def writeToTxtCover(self, file_path, content):
        with open(file_path, 'w') as txt_writer:
            txt_writer.write(str(content))
        txt_writer.close()

    def wash(self, in_path, out_path):
        in_files = os.listdir(in_path)
        count = 0
        for file in in_files:
            in_file_path = "{0}/{1}".format(in_path, file)
            out_file_path = "{0}/{1}".format(out_path, file)
            in_content_list = self.readFromTxt(in_file_path)
            if (len(in_content_list)) > 0:
                count += 1
                if count > 32000:
                    return
                out_content = in_content_list[0]
                self.writeToTxtCover(out_file_path, out_content)



if __name__ == "__main__":
    inpath = '/home/dev/Data/npl/classifier/fastText_huxiu_content/raw_data/ifeng/'
    outpath = '/home/dev/Data/npl/classifier/fastText_huxiu_content/raw_data/ifeng_washed/'
    washdata = WashData()
    washdata.wash(inpath, outpath)