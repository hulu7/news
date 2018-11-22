# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
import datetime
import codecs
import csv
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SendEmail():
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
            if len(content) > 0 and type(content) == type(content[0]):
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
        txt_file.close()
        return content

    def writeToTxt(self, file_path, content):
        with open(file_path, 'w') as txt_writer:
            txt_writer.write(str(content))
        txt_writer.close()

    def createEmailBody(self):
        cache_file = self.file_path + 'cache.txt'
        content_file = self.file_path + 'ifeng_content.csv'
        isCacheFileExists = os.path.exists(cache_file)
        self.isReadyToSend = False
        if isCacheFileExists is True:
            cache = int(self.readFromTxt(cache_file))
        else:
            cache = 0
        isContentFileExists = os.path.exists(content_file)
        if isContentFileExists is True:
            items_list = self.readFromCSV(content_file)
            cand_list = []
            for item in items_list:
                cand_list.append(item)
            if (cache + 400) < len(cand_list):
                self.isReadyToSend = True
                today = "".join(str(datetime.date.today()))
                time = "".join(str(datetime.datetime.now())[11:19])
                self.body = '<p></p>' + '<p>' + today + ' ' + time + '</p>' + '<p> 进度 : ' + str(len(cand_list)) + '</p>'
                for i in range(cache, cache + 400):
                    self.body = self.body + \
                           '<p>' + \
                           '<a href=' + cand_list[i][5] + '>' + \
                                cand_list[i][1] + \
                           '</a>' + \
                           '</p>'
                cache = cache + 400
                self.writeToTxt(cache_file, cache)
        else:
            self.isReadyToSend = False

    def send(self, file_path):
        self.file_path = file_path
        self.createEmailBody()
        if self.isReadyToSend is True:
            host = 'smtp.163.com'
            port = 465
            sender = 'hui_asus@163.com'
            pwd = 'thebest1990'
            receiver = 'hui_asus@163.com'
            msg = MIMEText(self.body, 'html')
            msg['subject'] = '进度监测'
            msg['from'] = sender
            msg['to'] = receiver
            try:
                s = smtplib.SMTP_SSL(host, port)
                s.login(sender, pwd)
                s.sendmail(sender, receiver, msg.as_string())
                print ('Done! Sent email success')
            except smtplib.SMTPException:
                print ('Error! Sent email fail')

if __name__ == '__main__':
    send = SendEmail()
    filePath = '/home/dev/Data/rsyncData/prd1/ifeng/'
    send.send(filePath)
