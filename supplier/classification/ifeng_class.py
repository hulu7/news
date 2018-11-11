# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import jieba
import time
import jieba.posseg as posseg
from shutil import copyfile
import deep
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateProductionClass():
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

    def extractKeyWords(self, content):
        text = content.decode("utf-8").encode("utf-8")
        seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
        outline = " ".join(seg_text)
        return outline

    def extractTime(self, content):
        toGBK = content.encode('gbk')
        getDigit = filter(str.isdigit, toGBK)
        getYMD = getDigit[0:8]
        return getYMD

    def loadModel(self):
        self.classifier = fasttext.load_model(self.model_path)

    def predictClass(self, content):
        keywords = self.extractKeyWords(content)
        return self.classifier.predict_proba([keywords], k=1)[0]

    def startClassify(self, txt_path, content_path, class_finished_path, model_path, log_path, catalogs, name):
        self.log_path = log_path
        self.content_path = content_path
        self.class_finished_path = class_finished_path
        self.model_path = model_path
        self.catalogs = catalogs
        self.txt_path = txt_path

        self.loadModel()
        content = self.readFromCSV(content_path)
        self.finishedIds = []
        for catalog in catalogs:
            catalog_path = self.class_finished_path + '/' + catalog + '/' + catalog + '.csv'
            catalog_cache_path = self.class_finished_path + '/' + catalog + '/cache/' + name + '_cache.csv'
            isCatalogFileExists = os.path.exists(catalog_path)
            isCatalogCacheFileExists = os.path.exists(catalog_cache_path)
            if isCatalogCacheFileExists is True:
                cache_list = self.readFromCSV(catalog_cache_path)
                for cache_item in cache_list[1:]:
                    self.finishedIds.append(str(cache_item[0].replace('\xef\xbb\xbf','')))
            else:
                self.writeToCSVWithoutHeader(catalog_cache_path, ['id'])
            if isCatalogFileExists is False:
                self.writeToCSVWithoutHeader(catalog_path, ['id', 'title', 'url', 'time', 'catalog', 'deep'])

        for item in content:
            if content.index(item) == 0:
                continue
            if item[6] not in self.finishedIds:
                file = name + '_' + item[6] + '_.txt'
                most_possible = self.predictClass(item[3])
                catalog = str(most_possible[0][0].split('__')[2])
                deep = dep.howDeep(self.txt_path + '/' + file)
                catalog_cache_path = self.class_finished_path + '/' + catalog + '/cache/' + name + '_cache.csv'
                catalog_path = self.class_finished_path + '/' + catalog + '/' + catalog + '.csv'
                YMD = self.extractTime(item[5])
                self.writeToCSVWithoutHeader(catalog_cache_path, [item[6]])
                self.finishedIds.append(item[6])
                self.writeToCSVWithoutHeader(catalog_path, [item[6], item[3], item[2], YMD, catalog, deep])
                origin_txt_path = self.txt_path + '/' + file
                classed_txt_path = self.class_finished_path + '/' + catalog + '/txt/' + file
                copyfile(origin_txt_path, classed_txt_path)

                time_elapsed = time.time() - since
                print(str(len(self.finishedIds)) + ' complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
        time_elapsed = time.time() - since
        print('Done! in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

if __name__ == "__main__":

    catalogs = ['agriculture','astrology','baby','buddhism','car','career',
                'comic','culture','design','digital','edu','emotion','collect',
                'entertainment','fashion','festival','finance','food','funny',
                'game','health','history','home','lottery','military','government',
                'pet', 'photography', 'politics', 'psychology', 'society', 'sports',
                'story', 'tech', 'technique', 'travel', 'house', 'life', 'wedding']
    txt_path = '/home/dev/Data/rsyncData/prd1/ifeng/txt'
    content_path = '/home/dev/Data/rsyncData/prd1/ifeng/ifeng_content.csv'
    class_finished_path = '/home/dev/Data/Production/catalogs'
    log_path = '/home/dev/Data/Production/log'
    model_path = '/home/dev/Data/npl/classifier/fastText/model_data/news_fasttext.model.bin'
    name = 'ifeng'

    print "start classify..."
    since = time.time()
    dep = deep.deepMax()
    update = UpdateProductionClass()
    update.startClassify(txt_path, content_path, class_finished_path, model_path, log_path, catalogs, name)