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
from bloomfilterOnRedis import BloomFilter
import redis

class UpdateProductionClass():
    def __init__(self):
        self.rconn = redis.Redis('127.0.0.1', 6379)
        self.bf = BloomFilter(self.rconn, 'supplier:classification')
        self.today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def isDuplicated(self, title):
        title_encode = str(title).encode("utf-8")
        if self.bf.isContains(title_encode):
            print 'Title {0} exists!'.format(title)
            return True
        else:
            self.bf.insert(title_encode)
            print 'Title {0} not exist!'.format(title)
            return False

    def storeFinished(self, title):
        print 'Start to store title: {0}'.format(title)
        title_encode = title.encode("utf-8")
        self.bf.insert(title_encode)

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

    def writeToTxt(self, filePath, content):
        with open(filePath, 'a+') as txt_file:
            txt_file.write(content)
            txt_file.write('\n')
        return txt_file.close()

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

    def getCurrntTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def loadModel(self, model_path):
        self.classifier = fasttext.load_model(model_path)

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
        isContentFileExists = os.path.exists(content_path)
        if isContentFileExists is False:
            return
        content = self.readFromCSV(content_path)
        self.finishedIds = []
        for catalog in catalogs:
            catalog_file_path = '{0}/{1}'.format(self.class_finished_path, catalog)
            catalog_cache_file_path = '{0}/{1}/cache'.format(self.class_finished_path, catalog)
            catalog_txt_file_path = '{0}/{1}/txt'.format(self.class_finished_path, catalog)
            isCatalogFilePathExists = os.path.exists(catalog_file_path)
            isFinishedFilePathExists = os.path.exists(self.class_finished_path)
            isCatalogCacheFilePathExists = os.path.exists(catalog_cache_file_path)
            isCatalogTxtFilePathExists = os.path.exists(catalog_txt_file_path)
            if isFinishedFilePathExists is False:
                os.mkdir(self.class_finished_path)
            if isCatalogFilePathExists is False:
                os.mkdir(catalog_file_path)
            if isCatalogCacheFilePathExists is False:
                os.mkdir(catalog_cache_file_path)
            if isCatalogTxtFilePathExists is False:
                os.mkdir(catalog_txt_file_path)
            catalog_path = '{0}/{1}/{2}_{3}.csv'.format(self.class_finished_path, catalog, self.today, catalog)
            catalog_cache_path = '{0}/{1}/cache/{2}_{3}_cache.csv'.format(self.class_finished_path, catalog, self.today, name)
            isCatalogFileExists = os.path.exists(catalog_path)
            isCatalogCacheFileExists = os.path.exists(catalog_cache_path)
            if isCatalogCacheFileExists is True:
                cache_list = self.readFromCSV(catalog_cache_path)
                for cache_item in cache_list[1:]:
                    self.finishedIds.append(str(cache_item[0].replace('\xef\xbb\xbf','')))
            else:
                self.writeToCSVWithoutHeader(catalog_cache_path, ['id'])
            if isCatalogFileExists is False:
                self.writeToCSVWithoutHeader(catalog_path, ['id', 'title', 'url', 'time', 'catalog', 'deep', 'is_open_cache', 'source', 'author_name', 'images'])
        total = '0'
        for item in content:
            if content.index(item) == 0:
                self.id_index = item.index('id')
                self.title_index = item.index('title')
                self.url_index = item.index('url')
                self.time_index = item.index('download_time')
                self.is_open_cache = item.index('is_open_cache')
                self.source = item.index('source')
                self.author_name = item.index('author_name')
                self.images = item.index('images')
                continue
            id = item[self.id_index]
            title = item[self.title_index]
            url = item[self.url_index]
            time_ = item[self.time_index]
            is_open_cache = item[self.is_open_cache]
            source = item[self.source]
            author_name = item[self.author_name]
            images = item[self.images]
            if len(title) == 0 or len(url) == 0 or len(time_) == 0:
                self.finishedIds.append(id)
                continue
            if self.isDuplicated(title) is False:
                file = '{0}_{1}.txt'.format(name, id)
                most_possible = self.predictClass(title)
                catalog = str(most_possible[0][0].split('__')[2])
                deep = dep.howDeep('{0}/{1}'.format(self.txt_path, file))
                if len(str(deep)) == 0:
                    self.writeToTxt(log_path, "{0}: empty {1}".format(str(update.getCurrntTime()), file))
                    continue
                catalog_cache_path = '{0}/{1}/cache/{2}_{3}_cache.csv'.format(self.class_finished_path, catalog, self.today, name)
                catalog_path = '{0}/{1}/{2}_{3}.csv'.format(self.class_finished_path, catalog, self.today, catalog)
                YMD = self.extractTime(time_)
                self.writeToCSVWithoutHeader(catalog_cache_path, [id])
                self.finishedIds.append(id)
                self.storeFinished(title)
                self.writeToCSVWithoutHeader(catalog_path, [id, title, url, YMD, catalog, deep, is_open_cache, source, author_name, images])
                origin_txt_path = '{0}/{1}'.format(self.txt_path, file)
                classed_txt_path = '{0}/{1}/txt/{2}'.format(self.class_finished_path, catalog, file)
                copyfile(origin_txt_path, classed_txt_path)

                time_elapsed = time.time() - since
                total = str(len(self.finishedIds))
                print(total + ' complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
        time_elapsed = time.time() - since
        self.writeToTxt(log_path, str(update.getCurrntTime() + ": " + total + ' classify done! in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60)))
        print 'classify done! in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60)

if __name__ == "__main__":

    catalogs = ['agriculture','astrology','baby','buddhism','car','career',
                'comic','culture','design','digital','edu','emotion','collect',
                'entertainment','fashion','festival','finance','food','funny',
                'game','health','history','home','lottery','military','government',
                'pet', 'photography', 'politics', 'psychology', 'society', 'sports',
                'story', 'tech', 'technique', 'travel', 'house', 'life', 'wedding']

    base_path = '/home/dev/Data/rsyncData/prd4'
    production_path = '/home/dev/Data/Production'
    model_path = '/home/dev/Data/npl/classifier/fastText/model_data/news_fasttext.model.bin'

    since = time.time()
    dep = deep.deepMax()
    update = UpdateProductionClass()
    update.loadModel(model_path)

    file_list = os.listdir(base_path)
    file_list.remove('log')
    for file in file_list:
        txt_path = '{0}/{1}/txt/{2}'.format(base_path, file, update.today)
        content_path = '{0}/{1}/{2}_content.csv'.format(base_path, file, file)
        class_finished_path = '{0}/catalogs'.format(production_path)
        log_path = '{0}/log/{1}_log.log'.format(production_path, update.today)
        name = file
        update.writeToTxt(log_path, '{0}: start classify: {1}'.format(str(update.getCurrntTime()), file))
        print 'start classify: {0}'.format(file)
        update.startClassify(txt_path, content_path, class_finished_path, model_path, log_path, catalogs, name)