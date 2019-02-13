# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import pandas as pd
import os
import sys
import shutil
import time
reload(sys)
sys.setdefaultencoding('utf-8')

class ProductionMerge():
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

    def getCatalog(self):

        return {
            'finance': '财经',
            'politics': '党政',
            'comic': '动漫',
            'house': '房产',
            'home': '家居',
            'health': '健康',
            'edu': '教育',
            'military': '军事',
            'tech': '科技',
            'history': '历史',
            'travel': '旅游',
            'food': '美食',
            'agriculture': '农业',
            'car': '汽车',
            'emotion': '情感',
            'design': '设计',
            'society': '社会',
            'photography': '摄影',
            'collect': '收藏',
            'digital': '数码',
            'sports': '体育',
            'culture': '文化',
            'game': '游戏',
            'entertainment': '娱乐',
            'baby': '育儿',
            'IT': 'IT互联网',
            'career': '职场',
            'life': '养生',
            'lottery': '彩票',
            'pet': '宠物',
            'fashion': '时尚',
            'festival': '节日',
            'funny': '幽默',
            'psychology': '心理',
            'story': '故事汇',
            'wedding': '婚礼',
            'Movie': '电影',
            'TV': '电视',
            'buddhism': '佛教',
            'government': '政府',
            'astrology': '星座'
        }

    def Merge(self, filein_path, fileout_path):

        today = time.strftime('%Y%m%d', time.localtime(time.time()))

        catalog = self.getCatalog()

        users = os.listdir(filein_path)

        out_csv_file = "{0}/{1}.csv".format(fileout_path, today)

        output_content = []

        finished_titles = []

        for user in users:

            in_csv_file = "{0}/{1}/{2}/{3}.csv".format(filein_path, user, today, today)

            isCsvExists = os.path.exists(in_csv_file)

            if isCsvExists is False:
                continue

            csv_content = self.readFromCSV(in_csv_file)

            if len(csv_content) < 2:

                continue

            isOutputPathExists = os.path.exists(out_csv_file)

            if isOutputPathExists is False:

                self.writeToCSVWithoutHeader(out_csv_file, ['title', 'url', 'time', 'catalog', 'user'])

            for item in csv_content[1:]:

                if item[1] in finished_titles:

                    for content in output_content:

                        if content[0] == item[1]:

                            if user not in content[4]:

                                content[4] = "{0},{1}".format(content[4], user)

                    continue

                if item[5] == '':

                    continue

                if item[3] == '':

                    item[3] = today

                output_content.append([item[1], item[2], item[3], catalog[item[4]], user])

                finished_titles.append(item[1])

        for content in output_content:

            self.writeToCSVWithoutHeader(out_csv_file, content)

if __name__ == "__main__":
    filein = '/home/dev/Data/Production/data4customers'
    fileout = '/home/dev/Data/Production/data4deepinews'
    flt = ProductionMerge()
    flt.Merge(filein, fileout)