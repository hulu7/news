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
        with open(filePath, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
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
            csv_writer.writerow(content)
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
        gzh = "公众号"
        pattern1 = "（ID："
        if gzh in sentence:
            if pattern1 in sentence:
                s1 = sentence.replace('\n', '').replace(' ', '')
                s2 = re.findall(r"公众号：(.+?)）",s1)
                s3 = re.findall(r"公众号“(.+?)）",s1)
                s4 = re.findall(r"公众号(.+?)）", s1)
                print '***{0}***'.format(s1)
                if (len(s2) != 0):
                    s2_1 = s2[0].split("（ID：")
                    if (len(s2_1) == 1):
                        name = s2_1[0]
                        extractGongzhonghao.writeToCSVWithoutHeader(to_path, [name, ''])
                        print '===name==={0}==='.format(name.decode("utf-8"))
                    else:
                        name = s2_1[0]
                        id = s2_1[1]
                        extractGongzhonghao.writeToCSVWithoutHeader(to_path, [name, id])
                        print '===name==={0}==='.format(name.decode("utf-8"))
                        print '===id==={0}==='.format(id.decode("utf-8"))
                elif (len(s3) != 0):
                    s3_1 = s3[0].split("”（ID：")
                    if (len(s3_1) == 1):
                        name = s3_1[0]
                        extractGongzhonghao.writeToCSVWithoutHeader(to_path, [name, ''])
                        print '---name---{0}---'.format(name.decode("utf-8"))
                    else:
                        name = s3_1[0]
                        id = s3_1[1]
                        extractGongzhonghao.writeToCSVWithoutHeader(to_path, [name, id])
                        print '---name---{0}---'.format(name.decode("utf-8"))
                        print '---id---{0}---'.format(id.decode("utf-8"))
                elif (len(s2) == 0 and len(s3) == 0 and len(s4) != 0):
                    s4_1 = s4[0].split("（ID：")
                    if (len(s4_1) == 1):
                        name = s4_1[0]
                        extractGongzhonghao.writeToCSVWithoutHeader(to_path, [name, ''])
                        print '###name###{0}###'.format(name.decode("utf-8"))
                    else:
                        name = s4_1[0]
                        id = s4_1[1]
                        extractGongzhonghao.writeToCSVWithoutHeader(to_path, [name, id])
                        print '###name###{0}###'.format(name.decode("utf-8"))
                        print '###id###{0}###'.format(id.decode("utf-8"))
                else:
                    print '$=={0}==='.format(s1)
                    extractGongzhonghao.writeToCSVWithoutHeader(to_path, [s1, ''])

    def deduplicate(self):
        print 'start to de dup'
        all_list = self.readFromCSV(from_dup)
        finished = []
        for item in all_list:
            if item[1] not in finished:
                self.writeToCSVWithoutHeader(to_dup, item)
                finished.append(item[1])
        print 'end to de dup'

if __name__ == '__main__':
    extractGongzhonghao = ExtractGongzhonghao()
    from_path = '/home/dev/Data/rsyncData/prd4/sites/huxiu/txt'
    to_path = '/home/dev/Data/rsyncData/prd4/sites/huxiu/gongzhonghao.csv'
    from_dup = '/home/dev/Data/rsyncData/prd4/sites/huxiu/dup.csv'
    to_dup = '/home/dev/Data/rsyncData/prd4/sites/huxiu/dup_result.csv'
    to_path_exists = os.path.exists(to_path)
    if to_path_exists is False:
        extractGongzhonghao.writeToCSVWithoutHeader(to_path,['name', 'id'])
    file_list = os.listdir(from_path)
    for file in file_list:
        txt_path = '{0}/{1}'.format(from_path, file)
        extractGongzhonghao.extract(txt_path, to_path)
    extractGongzhonghao.deduplicate()
    print 'done'