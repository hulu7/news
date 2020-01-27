#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
import gc
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class NoNameBone():

    def __init__(self, settingName, callback=callable):
        self.settingName = settingName
        self.callBack = callback
        self.globalSettings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings(self.settingName)
        self.log_path = self.globalSettings.LOG_PATH_PRD2
        self.author_path = self.settings.AUTHORS_PATH
        self.name = self.settings.NAME

    def store(self):
        result = self.callBack()
        if result == None:
            return
        print 'Start to store authors for page: {0}'.format(result.page_url)
        if len(result.authors) == 0:
            message1 = 'No author for page: {0}'.format(result.page_url)
            self.file.logger(self.log_path, message1)
            print message1
        for item in result.authors:
            is_title_empty = self.doraemon.isEmpty(item)
            if (is_title_empty is False) and (self.doraemon.isDuplicated(self.doraemon.bf_authors, item) is False):
                message2 = 'Start to store author: {0} for page: {1}.'.format(item, result.page_url)
                self.file.logger(self.log_path, message2)
                print message2
                self.doraemon.storeTxtAdd(self.author_path, item, self.settingName)
                message3 = 'Success to store author: {0} for page: {1}.'.format(item, result.page_url)
                self.file.logger(self.log_path, message3)
                print message3
            else:
                if is_title_empty is True:
                    message4 = 'Empty author for {0}'.format(result.page_url)
                    self.file.logger(self.log_path, message4)
                    print message4
                else:
                    message5 = 'Duplicated author for {0}'.format(result.page_url)
                    self.file.logger(self.log_path, message5)
                    print message5
        print 'End to store author: {0} for page: {1}.'.format(item, result.page_url)
        del result
        gc.collect()

if __name__ == '__main__':
    noNameBone=NoNameBone()
    noNameBone.store()