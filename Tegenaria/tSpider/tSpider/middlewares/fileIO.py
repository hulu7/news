#coding:utf-8
import datetime
import time
import codecs
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class File():
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
        txt_file.close()
        return content


    def writeToTxtCover(self, file_path, content):
        with open(file_path, 'w') as txt_writer:
            txt_writer.write(str(content))
        txt_writer.close()

    def writeToTxtAdd(self, file_path, content):
        with open(file_path, 'a') as txt_writer:
            txt_writer.write(str(content) + '\n')
        txt_writer.close()

    def logger(self, file_path, content):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.writeToTxtAdd(file_path, str(current_time + ": " + content))
