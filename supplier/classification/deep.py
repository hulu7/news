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

class deepMax():
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

    def howDeep(self, filePath):
        sentence_list = self.splitTxtToList(filePath)
        relationships = {}
        for sentence in sentence_list:
            nouns = []
            wordArray = posseg.cut(sentence)
            for w in wordArray:
                if ((w.flag == 'nr' or
                     w.flag == 'n' or
                     w.flag == 'vn' or
                     w.flag == 'eng' or
                     w.flag == 'vn' or
                     w.flag == 'ns') and len(w.word) >= 2):
                    nouns.append(w.word)
            self.relationShipsInSentence(relationships, nouns)
        return self.findDeepMax(relationships)

    def relationShipsInSentence(self, relationships, nouns):
        for noun_a in nouns:
            for noun_b in nouns:
                if noun_a == noun_b:
                    continue
                if relationships.get(noun_a) is None:
                    relationships[noun_a] = {}

                if relationships[noun_a].get(noun_b) is None:
                    relationships[noun_a][noun_b] = 1
                else:
                    relationships[noun_a][noun_b] = relationships[noun_a][noun_b] + 1
        return relationships

    def singleChain(self, relatonships_object, chain):
        for child_first_key in relatonships_object:
            if child_first_key == chain[len(chain) - 1]:
                child_object = relatonships_object[child_first_key]
                for child_second_key in child_object:
                    if child_second_key not in chain:
                        chain.append(child_second_key)
                        return self.singleChain(relatonships_object, chain)
        return chain

    def findDeepMax(self, relatonships_object):
        all_links = []
        deep = []
        for child_first_key in relatonships_object:
            chain = [child_first_key]
            all_links.append(self.singleChain(relatonships_object, chain))
        for link in all_links:
            deep.append(len(link))
        if len(deep) == 0:
            return
        averageDeep = sum(deep) / len(deep)
        return averageDeep

if __name__ == '__main__':
    deep = deepMax()
    deepMax = deep.howDeep('/home/dev/Data/backup/spiderNode1/files/huxiu/txt/huxiu_265211_.txt')
    print deepMax