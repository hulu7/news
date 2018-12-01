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
        ifeng_urls = self.file_path + 'ifeng/ifeng_urls.csv'
        isIfengUrlsExists = os.path.exists(ifeng_urls)
        huxiu_urls = self.file_path + 'huxiu/huxiu_urls.csv'
        isHuxiuUrlsExists = os.path.exists(huxiu_urls)
        self.isReadyToSend = False
        if isIfengUrlsExists is True:
            items_list = self.readFromCSV(ifeng_urls)
            send_list = []
            for item in items_list:
                send_list.append(item)
            if 0 < len(send_list):
                self.isReadyToSend = True
                today = "".join(str(datetime.date.today()))
                time = "".join(str(datetime.datetime.now())[11:19])
                self.body = '<p></p>' + '<p>' + today + ' ' + time + '</p>' + '<p> ifeng 进度 : ' + str(len(send_list)) + '</p>'
                for i in range(len(send_list) - 20, len(send_list)):
                    self.body = self.body + \
                           '<p>' + \
                           '<a href=' + send_list[i][3] + '>' + \
                                send_list[i][6] + \
                                '[' + send_list[i][2] + ']' + \
                           '</a>' + \
                           '</p>'
        if isHuxiuUrlsExists is True:
            items_list = self.readFromCSV(huxiu_urls)
            send_list = []
            for item in items_list[1:]:
                send_list.append(item)
            if 0 < len(send_list):
                self.isReadyToSend = True
                today = "".join(str(datetime.date.today()))
                time = "".join(str(datetime.datetime.now())[11:19])
                self.body = self.body + '<p></p>' + '<p>' + today + ' ' + time + '</p>' + '<p> huxiu 进度 : ' + str(len(send_list)) + '</p>'
                for i in range(len(send_list) - 20, len(send_list)):
                    self.body = self.body + \
                           '<p>' + \
                           '<a href=' + send_list[i][1] + '>' + \
                                send_list[i][2] + \
                           '</a>' + \
                           '</p>'

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
            msg['subject'] = 'pr3进度监测'
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
    filePath = '/home/dev/Data/rsyncData/prd3/'
    send.send(filePath)
