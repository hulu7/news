# coding:utf-8
import re
import json
import jieba
import jieba.posseg as posseg
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import csv
import os

class ExtractGongzhonghao():
    def readFromJson(self, filePath):
        with open(filePath, 'r') as json_file:
            content = json.loads(json_file)
        json_file.close()
        return content

    def readLinesFromTxt(self, filePath):
        with open(filePath, 'r') as txt_file:
            content = txt_file.readlines()
        txt_file.close()
        return content

    def readFromTxt(self, filePath):
        with open(filePath, 'r') as txt_file:
            content = txt_file.read()
        txt_file.close()
        return content

    def readFromCSV(self, filePath):
        with open(filePath, 'r') as csv_file:
            content = csv.reader(csv_file)
        csv_file.close()
        return content

    def writeToCSVWithHeader(self, filePath, content, header):
        with open(filePath, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            for item in content:
                csv_writer.writerow(item)
        return csv_file.close()

    def writeToCSVWithoutHeader(self, filePath, content):
        with open(filePath, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            for item in content:
                csv_writer.writerow(item)
        return csv_file.close()

    def writeToJson(self, filePath, content):
        with open(filePath, 'w') as json_file:
            json_file.write(json.dumps(content, ensure_ascii=False))
        return json_file.close()

    def writeToTxt(self, filePath, content):
        with open(filePath, 'w') as txt_file:
            txt_file.write(content)
        return txt_file.close()


    def splitTxtToList(self, filePath):
        content = self.readFromTxt(filePath)
        split_list = re.split('。|！|\!|\.|？|\?', content)
        return list(filter(None, split_list))

    def extract(self, filePath, to_path):
        sentence_list = self.splitTxtToList(filePath)
        for sentence in sentence_list:
            id = self.extractId(sentence)

    def extractId(self, sentence):
        gzh = "微信公众号"
        pattern1 = "（ID："
        if gzh in sentence:
            if pattern1 in sentence:
                print 'start--{0}--end'.format(sentence)
                print self.extractBracket(sentence)

    def extractBracket(self, sentence):
        return re.sub(r'[^\x00-\x7f]', '', sentence).replace('ID', '').strip()



if __name__ == '__main__':
    extractGongzhonghao = ExtractGongzhonghao()
    from_path = '/home/dev/Data/backup/spiderNode1/files/huxiu/txt'
    to_path = '/home/dev/Data/Production/customerInfo/source/huxiu.csv'
    to_path_exists = os.path.exists(to_path)
    if to_path_exists is False:
        extractGongzhonghao.writeToCSVWithoutHeader(to_path,['sentense', 'id'])
    file_list = os.listdir(from_path)
    for file in file_list:
        txt_path = '{0}/{1}'.format(from_path, file)
        extractGongzhonghao.extract(txt_path, to_path)
    print 'done'