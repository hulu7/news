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
        self.isReadyToSend = False
        all_pages = os.listdir(self.file_path)
        all_pages.remove('log')
        all_pages.remove('sp')
        today = "".join(str(datetime.date.today()))
        time = "".join(str(datetime.datetime.now())[11:19])
        self.body = '<p></p><p>{0} {1}</p><p> --------prd3-------- </p>'.format(today, time)
        for page in all_pages:
            page_file = '{0}/{1}/{2}_urls.csv'.format(self.file_path, page, page)
            isPageFileExists = os.path.exists(page_file)
            if isPageFileExists is True:
                items_list = self.readFromCSV(page_file)
                self.body = '{0}<p>{1} 进度 -- {2}</p>'.format(self.body, page, str(len(items_list) - 1))
        for page in all_pages:
            page_file = '{0}/{1}/{2}_urls.csv'.format(self.file_path, page, page)
            isPageFileExists = os.path.exists(page_file)
            if isPageFileExists is True:
                items_list = self.readFromCSV(page_file)
                send_list = []
                for item in items_list:
                    send_list.append(item)
                if 0 < len(send_list):
                    self.isReadyToSend = True
                    self.body = '{0}<p>-- {1} 最新消息 --</p>'.format(self.body, page)
                    for i in range(len(send_list) - 10, len(send_list)):
                        url = send_list[i][1]
                        title = send_list[i][2]
                        get_time = ""
                        self.body = '{0}<p><a href={1}>@ {2} {3}</a></p>'.format(self.body, url, title, get_time)

    def send(self, file_path):
        self.file_path = file_path
        self.createEmailBody()
        if self.isReadyToSend is True:
            host = 'smtp.163.com'
            port = 465
            sender = 'hui_asus@163.com'
            pwd = 'thebest1990'
            receiver = 'hui_asus@163.com'
            msg = MIMEText(self.body, 'html', 'utf-8')
            msg['subject'] = 'pr3进度监测'
            msg['from'] = sender
            msg['to'] = receiver
            msg["Accept-Language"] = 'zh-CN'
            msg["Accept-Charset"] = 'ISO-8859-1,utf-8'
            try:
                s = smtplib.SMTP_SSL(host, port)
                s.login(sender, pwd)
                s.sendmail(sender, receiver, msg.as_string())
                print ('Done! Sent email success')
            except smtplib.SMTPException:
                print ('Error! Sent email fail')

if __name__ == '__main__':
    send = SendEmail()
    filePath = '/home/dev/Data/rsyncData/prd3'
    send.send(filePath)
