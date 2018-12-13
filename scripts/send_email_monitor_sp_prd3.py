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
        sp_urls = self.file_path + 'sp/sp_urls.csv'
        sent_urls = self.file_path + 'sp/sp_sent_urls.csv'
        isSpUrlsExists = os.path.exists(sp_urls)
        isSpSentIdsExists = os.path.exists(sent_urls)
        self.isReadyToSend = False
        if isSpSentIdsExists is False:
            self.writeToCSVWithoutHeader(sent_urls, ['id'])
        sent_ids = self.readFromCSV(sent_urls)
        if isSpUrlsExists is True:
            items_list = self.readFromCSV(sp_urls)
            if len(sent_ids) != len(items_list):
                send_list = []
                for item in items_list:
                    if [str(item[0])] not in sent_ids:
                        send_list.append(item)
                        self.writeToCSVWithoutHeader(sent_urls, [str(item[0])])
                if 0 < len(send_list):
                    self.isReadyToSend = True
                    today = "".join(str(datetime.date.today()))
                    time = "".join(str(datetime.datetime.now())[11:19])
                    self.body = '<p>{0} {1} 龙华园新上房源 </p>'.format(today, time)
                    for i in range(len(sent_ids) - 1, len(send_list)):
                        self.body = '{0}<p><a href= {1}>[{2}] {3} [价格 - {4} 万]</a></p>'.format(self.body, send_list[i][2], str(i - len(sent_ids) + 2), send_list[i][1], send_list[i][3])

    def send(self, file_path):
        self.file_path = file_path
        self.createEmailBody()
        if self.isReadyToSend is True:
            receivers = ['hui_asus@163.com', 'liusk92@163.com']
            for receiver in receivers:
                host = 'smtp.163.com'
                port = 465
                sender = 'hui_asus@163.com'
                pwd = 'thebest1990'
                msg = MIMEText(self.body, 'html', 'utf-8')
                msg['subject'] = 'pr3-龙华园新上房源'
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
    filePath = '/home/dev/Data/rsyncData/prd3/'
    send.send(filePath)
