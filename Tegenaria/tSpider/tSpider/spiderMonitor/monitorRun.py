#coding:utf-8
import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon
from Tegenaria.tSpider.tSpider.spiderMonitor.updateMonitorFiles import UpdateMonitorFiles

class MonitorRun():
    def __init__(self, isdebug=False):
        self.isDebug = isdebug
        self.doraemon = Doraemon()
        self.sites_info = self.doraemon.getSitesInfo(isdebug=self.isDebug)

    def start(self):
        try:
            allSitesData = []
            for site in self.sites_info:
                print 'start to update monitor files for spider: {0}'.format(site.name)
                monitor = UpdateMonitorFiles(site)
                allSitesData.append(monitor.processSingleSite())
            monitor.processAllSites(allSitesData)


        except Exception as e:
            print 'Exception: {0} for monitor file of spider {1}'.format(e.message, site.name)

if __name__ == '__main__':
    monitorRun = MonitorRun(isdebug=False)
    monitorRun.start()