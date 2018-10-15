# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from time import sleep
def sentemail():
    host = 'smtp.163.com'
    port = 465
    sender = 'hui_asus@163.com'
    pwd = 'thebest1990'
    receiver = 'huiskai@qq.com'
    url_download=open('//home//dev//Backups//prd1//files//ifeng//url//cache//cache.txt', 'r')
    url_status=url_download.read()
    url_download.close()
    content_download=open('//home//dev//Backups//prd1//files//ifeng//data//cache//cache.txt', 'r')
    content_status=content_download.read()
    content_download.close()
    body = '<p>Url Status:</p>' + '<p>'+ url_status +'</p>' + '<p>Content Status:</p>' + '<p>'+ content_status +'</p>'
    msg = MIMEText(body, 'html')
    msg['subject'] = 'ifeng status'
    msg['from'] = sender
    msg['to'] = receiver
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        print ('Done.sent email success')
    except smtplib.SMTPException:
        print ('Error.sent email fail')


if __name__ == '__main__':
    sentemail()
