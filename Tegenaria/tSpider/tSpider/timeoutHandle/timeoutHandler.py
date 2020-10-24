# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import psutil
import os
import signal
import time
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.dto.dto import ProcessTimeoutDto

class ProcessTimeoutHandler():
    def __init__(self):
        self.doraemon = Doraemon()
        self.file = FileIOMiddleware()
        self.settings = Settings()

        self.cache_file = self.settings.TIMEOUT_CACHE_FILE
        self.timeout = self.settings.PROCESS_TIMEOUT

    def updateTimeoutCacheFile(self, processes):
        if self.doraemon.isFileExists(self.cache_file):
            self.doraemon.deleteFile(self.cache_file)
        for process in processes:
            tmp = '{0}-{1}'.format(process.pid, process.past)
            self.file.writeToTxtAdd(self.cache_file, tmp)

    def getTimeoutCache(self):
        result = []
        if self.doraemon.isFileExists(self.cache_file):
            data = self.file.readFromTxt(self.cache_file)
            pidTimeoutList = data.split('\n')
            for item in pidTimeoutList:
                if self.doraemon.isEmpty(item) is False:
                    tmp = item.split('-')
                    if len(tmp) == 2:
                        result.append(ProcessTimeoutDto(
                            int(tmp[0]),
                            float(tmp[1]),
                            False
                        ))
        return result

    def findTarget(self, pid, pids):
        result = None
        for p in pids:
            if p.pid == pid:
                result = p
        return result

    def filterTimeoutProcesses(self, curpids, prepids):
        result = []
        if self.doraemon.isEmpty(curpids):
            return result
        for p in curpids:
            pre = self.findTarget(p.pid, prepids)
            if pre is not None and self.doraemon.isExceedTimeoutInterval(self.timeout, pre.past):
                result.append(ProcessTimeoutDto(
                    pre.pid,
                    pre.past,
                    True
                ))
            else:
                result.append(p)
        return result

    def getCurrentProcesses(self):
        result = []
        pids = psutil.pids()
        if len(pids):
            print 'No Chrome process.'
        for pid in pids:
            try:
                p = psutil.Process(pid)
                if p.name() == 'chrome':
                    print 'Start to store process {0}.'.format(pid)
                    result.append(ProcessTimeoutDto(
                        pid,
                        p._create_time,
                        False
                    ))
            except Exception as e:
                print 'Exception {0} to find process: pid - {1}'.format(e, p.pid)
        return result

    def processTimeoutProcesses(self, curpids, prepids):
        updatedPids = self.filterTimeoutProcesses(curpids, prepids)
        notTimeoutProcesses = []
        for p in updatedPids:
            if p.isTimeout:
                try:
                    print 'kill timeout process: pid - {0}'.format(p.pid)
                    os.kill(p.pid, signal.SIGKILL)
                except Exception as e:
                    print 'Exception {0} to kill process: pid - {1}'.format(e, p.pid)
            else:
                notTimeoutProcesses.append(p)
        self.updateTimeoutCacheFile(notTimeoutProcesses)


    def start(self):
        print 'Start to process.'
        self.processTimeoutProcesses(self.getCurrentProcesses(), self.getTimeoutCache())

if __name__ == '__main__':
    handler=ProcessTimeoutHandler()
    handler.start()