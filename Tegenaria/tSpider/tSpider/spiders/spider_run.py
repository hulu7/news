#coding:utf-8
import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
from multiprocessing.pool import ThreadPool as Pool
import gc
import time
from Tegenaria.tSpider.tSpider.spiders.spider_content import Spider
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class SpiderRun():
    def __init__(self, isdebug=False):
        self.isDebug = isdebug
        self.doraemon = Doraemon()
        self.sites_info = self.doraemon.getSitesInfo(isdebug=self.isDebug)

    def runTask(self, site):
        time.sleep(1)
        try:
            print 'start to run content spider: {0}'.format(site.name)
            spider = Spider(site)
            spider.spiderBone.start()
        except Exception as e:
            print 'Exception: {0} for content spider {1}'.format(e.message, site.name)

    def applyMultiRun(self):
        poolSize = self.doraemon.max_concurrency_spider
        if self.isDebug:
            poolSize = 1
        process = Pool(poolSize)
        for site in self.sites_info:
            process.apply_async(self.runTask, args=(site,))
        process.close()
        process.join()
        if self.isDebug is False:
            self.applyMultiRun()

    def start(self):
        if self.isDebug:
            self.applyMultiRun()
        else:
            while(True):
                self.applyMultiRun()

if __name__ == '__main__':
    spiderRun = SpiderRun(isdebug=False)
    spiderRun.start()