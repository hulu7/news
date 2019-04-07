# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from lxml import etree
import urlparse
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.mongodbMiddleware import MongoMiddleware
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Dup():
    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()

    def getSettings(self):
        self.work_path = "//home//dev//Data//rsyncData//"
        self.finished_ids = "gongzhonghao_test"

    def startFilter(self):
        in_file1 = "{0}//gongzhonghao_test.txt".format(self.work_path)
        in_file2 = "{0}//gongzhonghao_available.txt".format(self.work_path)
        in_file3 = "{0}//gongzhonghao_test.csv".format(self.work_path)
        out_file1 = "{0}//gongzhonghao_uavailable.csv".format(self.work_path)
        out_file2 = "{0}//gongzhonghao_available.csv".format(self.work_path)
        dup_file = "{0}//dup_result.csv".format(self.work_path)
        all_content_dup = self.file.readFromTxt(in_file1)
        available_content = self.file.readFromTxt(in_file2)
        dup_content = self.file.readFromCSV(dup_file)
        available_list = available_content.split('\n')
        all_list_dup = all_content_dup.split('\n')
        available_content_dup = self.file.readFromCSV(in_file3)
        all_list = []
        for i in all_list_dup:
            if i not in all_list:
                all_list.append(i)

        all_compare = []
        available_compare = []
        for i in all_list:
            if self.doraemon.isEmpty(i) is False:
                all_compare.append(i.strip())
        for i in available_list:
            if self.doraemon.isEmpty(i) is False:
                available_compare.append(i.strip())

        dup_items_unavailable = []
        dup_items_available = []
        for item_all in all_compare:
            if item_all not in available_compare:
                for i in dup_content:
                    if i[1] == item_all and i[1] not in dup_items_unavailable:
                        self.file.writeToCSVWithoutHeader(out_file1, i)
                        dup_items_unavailable.append(item_all)
                print item_all
            else:
                for i in available_content_dup:
                    if i[1] == item_all and item_all not in dup_items_available:
                        self.file.writeToCSVWithoutHeader(out_file2, i)
                        dup_items_available.append(item_all)

if __name__ == '__main__':
    d=Dup()
    d.startFilter()