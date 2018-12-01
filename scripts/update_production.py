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


    def loadModel(self):
        self.classifier = fasttext.load_model(self.model_path)

    def predictClass(self, filein_path, fileout_path, model_path):
        self.model_path = model_path
        self.loadModel()
        content_list = self.readFromCSV(filein_path)
        for content in content_list:
            if content_list.index(content) == 0:
                continue
            keywords = self.extractKeyWords(content[6])
            classes = self.classifier.predict_proba([keywords], k=1)[0]
            catalogs = []
            for catalog in classes:
                catalogs.append(str(catalog[0].split('__')[2]))
                catalogs.append(str(catalog[1]))
            save_items = [content[4], content[6], content[3], content[5]] + catalogs
            save_header = ['id', 'title', 'url', 'imageUrl', 'most', 'mostPossible']

            isOutputFileExists = os.path.exists(fileout_path)
            if isOutputFileExists is True:
                self.writeToCSVWithoutHeader(fileout_path, save_items)
            else:
                self.writeToCSVWithHeader(fileout_path, save_items, save_header)

if __name__ == "__main__":
    filein = '/home/dev/Production/class/file_after_filter.csv'
    model = '/home/dev/Repository_Test_Data/classifier/fastText/model_data/news_fasttext.model.bin'
    fileout = '/home/dev/Production/class/classes.csv'
    update = UpdateProductionClass()
    update.predictClass(filein, fileout, model)