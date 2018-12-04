# -*- coding: utf-8 -*-
#------requirement------
#------requirement------
import os
import time
import gc
import smtplib
from email.mime.text import MIMEText
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.fileIOMiddleware import FileIOMiddleware
from settings import Settings

class Chronus():
    def init(self):
        self.getHourMinute()
        self.getDate()
        self.file = FileIOMiddleware()
        self.table_path = Settings.CHRONUS_SETTINGS
        self.base_path = Settings.RSYNC_PRD1

    def createEmailBody(self):
        self.isReadyToSend = False
        if len(self.static) < 2:
            return
        self.body = '<div>--------Chronus {0} {1} -------- </div>'.format(self.YearMonthDay, self.hourMinute)
        self.body = '{0}<div>Total {1} Increase {2} for {3} app</div>'.format(self.body ,str(self.total), str(self.increase_sum), str(len(self.pre) - 1))
        self.body = '{0}<div>{1} -- {2} -- {3} -- {4}</div>'.format(self.body, 'Name', 'Pre', 'Now', 'Increase')
        self.isReadyToSend = True
        for i in range(1, len(self.static)):
            self.body = '{0}<div>{1} -- {2} -- {3} -- {4}</div>'.format(self.body, self.header[i], self.pre[i], self.data[i], self.static[i])

    def collectStatisticData(self):
        files = os.listdir(self.base_path)
        files.remove('log')
        if 'chronus.csv' in files:
            files.remove('chronus.csv')
            previousData = self.file.readFromCSV(self.table_path)
        else:
            previousData = [['time']]
            previousData[0].extend(files)
            previousData.append([self.YearMonthDay])
            previousData[1].extend([0 for i in range(len(files))])
        self.data = [str(self.YearMonthDay)]
        for file in files:
            file_path = "{0}//{1}//{2}_content.csv".format(self.base_path, file, file)
            content = self.file.readFromCSV(file_path)
            self.data.append(str(len(content) - 1))
            print file + ' ' + str(len(content) - 1)
        self.header = previousData[len(previousData) - 2]
        self.pre = previousData[len(previousData) - 1]
        self.static = [self.pre[0]]
        self.increase_sum = 0
        self.total = 0
        for i in range(1, len(self.pre)):
            self.total = self.total + int(self.data[i])
            increase = int(self.data[i]) - int(self.pre[i])
            self.increase_sum = self.increase_sum + increase
            self.static.append(str(increase))

    def getHourMinute(self):
        self.hourMinute = time.strftime('%H:%M', time.localtime(time.time()))

    def getDate(self):
        self.YearMonthDay = time.strftime('%Y-%m-%d ', time.localtime(time.time()))

    def updateTable(self):
        files = os.listdir(self.base_path)
        files.remove('log')
        data = [str(self.YearMonthDay)]
        header = ["time"]
        header.extend(files)
        self.file.writeToCSVWithoutHeader(self.table_path, header)
        for file in files:
            file_path = "{0}//{1}//{2}_content.csv".format(self.base_path, file, file)
            content = self.file.readFromCSV(file_path)
            data.append(str(len(content)))
            print '{0} {1}'.format(file, str(len(content)))
        self.file.writeToCSVWithoutHeader(self.table_path, self.data)

    def sendEmail(self):
        self.createEmailBody()
        if self.isReadyToSend is True:
            host = 'smtp.163.com'
            port = 465
            sender = 'hui_asus@163.com'
            pwd = 'thebest1990'
            receiver = 'hui_asus@163.com'
            msg = MIMEText(self.body, 'html')
            msg['subject'] = 'pr4 chronus'
            msg['from'] = sender
            msg['to'] = receiver
            try:
                s = smtplib.SMTP_SSL(host, port)
                s.login(sender, pwd)
                s.sendmail(sender, receiver, msg.as_string())
                print ('Done! Sent email success')
            except smtplib.SMTPException:
                print ('Error! Sent email fail')

    def report(self):
        self.collectStatisticData()
        self.sendEmail()

    def run_chronus(self):
        self.init()
        print 'Now time is {0}'.format(self.hourMinute)
        self.report()
        print 'End report'
        if self.hourMinute == "18:00":
            print 'Start to store table'
            self.updateTable()
            print 'End to update table'
        del self
        gc.collect()

if __name__ == '__main__':
    chronus=Chronus()
    chronus.run_chronus()