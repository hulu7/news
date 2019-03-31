# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
from lxml import etree
import urlparse
from settings import Settings
from middlewares.mongodbMiddleware import MongoMiddleware
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.doraemonMiddleware import Doraemon

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
        out_file1 = "{0}//gongzhonghao_uavailable.txt".format(self.work_path)
        all_content = self.file.readFromTxt(in_file1)
        available_content = self.file.readFromTxt(in_file1)

        all_list = all_content.split('\n')
        available_list = available_content.split('\n')

        for item in all_list:
            if self.doraemon.isEmpty(item) is False:
                new_urls.append([url, ''])


if __name__ == '__main__':
    d=Dup()
    d.startFilter()