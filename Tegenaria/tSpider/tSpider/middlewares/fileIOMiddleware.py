#coding:utf-8
#------requirement------
#pandas-0.23.4
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import fcntl
import time
import codecs
import csv
import gc
import pandas as pd

class FileIOMiddleware():
    def readFromCSV(self, filePath):
        content = []
        with open(filePath, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        del scv_file
        gc.collect()
        return content

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def writeToCSVWithHeader(self, filePath, content, header):
        with open(filePath, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            if len(content) > 0 and type(content) == type(content[0]):
                for item in content:
                    csv_writer.writerow(item)
            else:
                csv_writer.writerow(content)
        csv_file.close()
        del csv_file
        gc.collect()

    def writeToCSVWithoutHeader(self, filePath, content):
        with open(filePath, 'a') as csv_file:
            fcntl.flock(csv_file.fileno(), fcntl.LOCK_EX)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(content)
        csv_file.close()
        del csv_file
        gc.collect()

    def readFromTxt(self, file_path):
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
        txt_file.close()
        del txt_file
        gc.collect()
        return content

    def writeToTxtCover(self, file_path, content):
        with open(file_path, 'w') as txt_writer:
            txt_writer.write(str(content))
        txt_writer.close()
        del txt_writer
        gc.collect()

    def writeToTxtAdd(self, file_path, content):
        with open(file_path, 'a') as txt_writer:
            txt_writer.write(str(content) + '\n')
        txt_writer.close()
        del txt_writer
        gc.collect()

    def logger(self, file_path, content):
        local_time = time.localtime(time.time())
        today = time.strftime('%Y-%m-%d', local_time)
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        self.writeToTxtAdd(file_path + '//' + today + '_log.log', str(current_time + ": " + content))
        del local_time, today, current_time
        gc.collect()