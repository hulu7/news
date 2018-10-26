# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from time import sleep
def sentemail():
    host = 'smtp.163.com'
    port = 465
    sender = 'zixun18@163.com'
    pwd = 'thebest1990'
    receiver = 'zixun18@163.com'
    base_path = '//home//dev//Repository_Test_Data//ifeng//log//'
    ient_file=open(base_path + 'ient//cache.txt', 'r')
    ient_log=ient_file.read()
    ient_file.close()
    ifashion_file=open(base_path + 'ifashion//cache.txt', 'r')
    ifashion_log=ifashion_file.read()
    ifashion_file.close()
    ifinance_file=open(base_path + 'ifinance//cache.txt', 'r')
    ifinance_log=ifinance_file.read()
    ifinance_file.close()
    ihistory_file=open(base_path + 'ihistory//cache.txt', 'r')
    ihistory_log=ihistory_file.read()
    ihistory_file.close()
    imil_file=open(base_path + 'imil//cache.txt', 'r')
    imil_log=imil_file.read()
    imil_file.close()
    inews_file=open(base_path + 'inews//cache.txt', 'r')
    inews_log=inews_file.read()
    inews_file.close()
    isports_file=open(base_path + 'isports//cache.txt', 'r')
    isports_log=isports_file.read()
    isports_file.close()
    itech_file=open(base_path + 'itech//cache.txt', 'r')
    itech_log=itech_file.read()
    itech_file.close()
    body = '<p>娱乐:</p>' + '<p>'+ ient_log +'</p>' + \
           '<div></div>' + \
           '<p>时尚:</p>' + '<p>' + ifashion_log + '</p>' + \
           '<div></div>' + \
           '<p>金融:</p>' + '<p>' + ifinance_log + '</p>' + \
           '<div></div>' + \
           '<p>历史:</p>' + '<p>' + ihistory_log + '</p>' + \
           '<div></div>' + \
           '<p>军事:</p>' + '<p>' + imil_log + '</p>' + \
           '<div></div>' + \
           '<p>新闻:</p>' + '<p>' + inews_log + '</p>' + \
           '<div></div>' + \
           '<p>体育:</p>' + '<p>' + isports_log + '</p>' + \
           '<div></div>' + \
           '<p>科技:</p>' + '<p>' + itech_log + '</p>' + \
           '<div></div>'
    msg = MIMEText(body, 'html')
    msg['subject'] = 'ifeng status'
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
    sentemail()
