# -*- coding:utf-8 -*-
import sys
reload(sys)
import os
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Recovery():
    def __init__(self):
        self.settings = Settings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.root = '/home/dev/Data/rsyncData/prd4/sites'
        self.dest = '/home/dev/Data/rsyncData/prd4/local'
        self.resume = '/home/dev/Repository/news/Tegenaria/tSpider/tSpider/dataRecovery/resume.txt'

    def start(self):
        sites = os.listdir(self.root)
        if os.path.exists(self.resume) is False:
            print 'resume file does not exit and create an new one'
            self.file.writeToTxtCover(self.resume, '\n')
        finished = []
        items = self.file.readFromTxt(self.resume).strip().split('\n')
        for item in items:
            finished.append(item)
        for site in sites:
            p1 = '{0}/{1}/html'.format(self.root, site)
            if os.path.exists(p1) is False:
                print '{0} has no html.'.format(site)
                continue
            allTime = os.listdir(p1)
            for t in allTime:
                p2 = '{0}/{1}'.format(p1, t)
                files = os.listdir(p2)
                for file in files:
                    fromFile = '{0}/{1}'.format(p2, file)
                    if fromFile not in finished:
                        toFile = '{0}/{1}'.format(self.dest, file)
                        if self.doraemon.copyFile(fromFile, toFile):
                            self.file.writeToTxtAdd(self.resume, fromFile)
                            print '{0} is recovered.'.format(fromFile)
            print '{0} is finished.'.format(site)

if __name__ == '__main__':
    r=Recovery()
    r.start()