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
        class_file = self.file_path + 'classes.csv'
        isCacheFileExists = os.path.exists(cache_file)
        if isCacheFileExists is True:
            cache = int(self.readFromTxt(cache_file))
        else:
            cache = 0
        isClassFileExists = os.path.exists(class_file)
        if isClassFileExists is True:
            items_list = self.readFromCSV(class_file)
            cand_list = []
            for item in items_list:
                if item[4] == 'house':
                    cand_list.append(item)
            if (cache + 10) < len(cand_list):
                self.isReadyToSend = True
                today = "".join(str(datetime.date.today()))
                time = "".join(str(datetime.datetime.now())[11:19])
                self.body = '<p>房地产最新新闻</p>' + '<p>' + today + '</p>'
                for i in range(cache, cache + 10):
                    self.body = self.body + \
                           '<p>' + \
                           '<a href=' + cand_list[i][2] + '>' + \
                                cand_list[i][1] + \
                           '</a>' + \
                           '</p>'
                cache = cache + 10
                self.writeToTxt(cache_file, cache)
        else:
            self.isReadyToSend = False



    def send(self, file_path):
        self.file_path = file_path
        self.createEmailBody()
        host = 'smtp.163.com'
        port = 465
        sender = 'hui_asus@163.com'
        pwd = 'thebest1990'
        receiver = '@qq.com'
        msg = MIMEText(self.body, 'html')
        msg['subject'] = '来自丑宝的推荐-房地产最新消息'
        msg['from'] = sender
        msg['to'] = receiver
        if self.isReadyToSend is True:
            try:
                s = smtplib.SMTP_SSL(host, port)
                s.login(sender, pwd)
                s.sendmail(sender, receiver, msg.as_string())
                print ('Done! Sent email success')
            except smtplib.SMTPException:
                print ('Error! Sent email fail')

if __name__ == '__main__':
    send = SendEmail()
    filePath = '/home/dev/Production/class/'
    send.send(filePath)
