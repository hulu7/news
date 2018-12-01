# _*_coding:utf-8 _*_
import fasttext
import codecs
import csv
import re
import xlrd
import time
from datetime import datetime, date, timedelta
from shutil import copyfile
import smtplib
from email.mime.text import MIMEText
import pandas as pd
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SendData():
    def readFromCSV(self, filePath):
        content = []
        with open(filePath, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def readColsFromCSV(self, file_path, col_names):
        cols = pd.read_csv(file_path, usecols=col_names)
        return cols

    def writeToCSVWithHeader(self, filePath, content, header):
        with open(filePath, 'a') as csv_file:
            csv_file.write(codecs.BOM_UTF8)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            if type(content) == type(content[0]):
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
            split_list = re.split('\n', content)
        txt_file.close()
        return list(filter(None, split_list))

    def writeToTxt(self, filePath, content):
        with open(filePath, 'a+') as txt_file:
            txt_file.write(content)
            txt_file.write('\n')
        return txt_file.close()

    def extractTime(self, content):
        toGBK = content.encode('gbk')
        getDigit = filter(str.isdigit, toGBK)
        getYMD = getDigit[0:8]
        return getYMD

    def readOneLineFromExcel(self, file_path, sheet_name, line):
        sheets = xlrd.open_workbook(file_path)
        table = sheets.sheet_by_name(sheet_name)
        return table.row_values(line)

    def readAllLinesFromExcel(self, file_path, sheet_name):
        sheets = xlrd.open_workbook(file_path)
        table = sheets.sheet_by_name(sheet_name)
        all_lines = []
        for row in range(1, table.nrows):
            all_lines.append(table.row_values(row))
        return all_lines

    def getCurrntTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def rankDeepByDecrease(self, array, col):
        return sorted(array, key=lambda x:x[col], reverse=True)

    def createEmailBody(self, customer_catalogs, data_to_send):
        if len(data_to_send) == 0:
            self.isReadyToSend = False
            return
        else:
            self.isReadyToSend = True
            self.body = '<p>' + self.getCurrntTime() + '</p>'
            for catalog in customer_catalogs:
                self.body = self.body + '<p>' + catalog + '</p>'
                for data in data_to_send:
                    if data[4] == catalog:
                        self.body = self.body + \
                                    '<p>' + \
                                    '<a href=' + data[2] + '>' + \
                                        data[1] + \
                                    '</a>' + \
                                    '</p>'

    def sendEmail(self, customer_email, customer_service_email, customer_catalogs, data_to_send):
        self.createEmailBody(customer_catalogs, data_to_send)
        host = 'smtp.163.com'
        port = 465
        sender = customer_service_email
        pwd = 'thebest1990'
        receiver = customer_email
        msg = MIMEText(str(self.body), 'html')
        msg['subject'] = "丑宝-房地产最新消息"
        msg['from'] = sender
        msg['to'] = receiver
        if self.isReadyToSend is True:
            try:
                s = smtplib.SMTP_SSL(host, port)
                s.login(sender, pwd)
                s.sendmail(sender, receiver, msg.as_string())
                self.writeToTxt(self.log_path, str(self.getCurrntTime() + ": " + customer_email + ' send email success! '))
                print str(self.getCurrntTime() + ": " + customer_email + ' send email success! ')
            except smtplib.SMTPException:
                self.writeToTxt(self.log_path, str(self.getCurrntTime() + ": " + customer_email + ' send email failed! '))
                print str(self.getCurrntTime() + ": " + customer_email + ' send email failed! ')

    def startSend(self, customer_info_path, data4customers_path, log_path, today, yesterday):
        self.customer_info_path = customer_info_path
        self.data4customers_path = data4customers_path
        self.log_path = log_path
        self.today = today
        self.yesterday = yesterday

        customers = self.readAllLinesFromExcel(customer_info_path, 'Sheet1')
        for customer in customers:
            customer_id = customer[0]
            customer_email = customer[2]
            customer_catalogs = customer[3].split(',')
            customer_keywords = customer[5].split(',')
            customer_service_email = customer[6]
            if len(str(customer[7])) == 0:
                customer_deep = 0
            else:
                customer_deep = int(customer[7])

            committed_data_file = self.data4customers_path + '/' + customer_id + '/' + self.yesterday + '/' + self.yesterday + '.csv'
            committed_data_file_exists = os.path.exists(committed_data_file)
            if committed_data_file_exists is False:
                self.isReadyToSend = False
                self.writeToTxt(self.log_path, str(self.getCurrntTime() + ": " + customer_email + ' no commited data! '))
                return
            committed_data = self.readFromCSV(committed_data_file)
            if len(committed_data) < 2:
                self.isReadyToSend = False
                self.writeToTxt(self.log_path, str(self.getCurrntTime() + ": " + customer_email + ' no rank commited data! '))
                return
            rank_committed_data = self.rankDeepByDecrease(committed_data[1:], 5)
            send_data_file = self.data4customers_path + '/' + customer_id + '/' + self.yesterday + '/' + self.yesterday + '_send.csv'
            send_data_file_exists = os.path.exists(send_data_file)
            if send_data_file_exists is False:
                self.writeToCSVWithoutHeader(send_data_file, ['id', 'title', 'url', 'time', 'catalog', 'deep'])
            data_to_send = []
            for data in rank_committed_data:
                if int(data[5]) > customer_deep:
                    if len(customer_keywords) > 1:
                        for key in customer_keywords:
                            if key in data[1]:
                                data_to_send.append(data)
                                self.writeToCSVWithoutHeader(send_data_file, data)
                                break
                    else:
                        data_to_send.append(data)
                        self.writeToCSVWithoutHeader(send_data_file, data)

            self.sendEmail(customer_email, customer_service_email, customer_catalogs, data_to_send)


if __name__ == "__main__":

    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    yesterday = (date.today() + timedelta(days = -1)).strftime("%Y%m%d")
    log_path = '/home/dev/Data/Production/log/' + today + '.log'
    customer_info_path = '/home/dev/Data/Production/customerInfo/customers.xlsx'
    data4customers_path = '/home/dev/Data/Production/data4customers'

    since = time.time()
    send = SendData()
    send.writeToTxt(log_path, str(send.getCurrntTime() + ": start send email..."))
    print "start send email..."
    send.startSend(customer_info_path, data4customers_path, log_path, today, yesterday)