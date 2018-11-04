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
    base_path = '//home//dev//rsyncData//prd2//ifeng//log//'

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

    iculture_file=open(base_path + 'iculture//cache.txt', 'r')
    iculture_log=iculture_file.read()
    iculture_file.close()

    ibook_file=open(base_path + 'ibook//cache.txt', 'r')
    ibook_log=ibook_file.read()
    ibook_file.close()

    body = '<div>------------Prd1------------</div>' + \
           '<div>' + ient_log + '</div>' + \
           '<div>' + ifashion_log + '</div>' + \
           '<div>' + ifinance_log + '</div>' + \
           '<div>' + ihistory_log + '</div>' + \
           '<div>' + imil_log + '</div>' + \
           '<div>' + inews_log + '</div>' + \
           '<div>' + isports_log + '</div>' + \
           '<div>' + itech_log + '</div>' + \
           '<div>' + iculture_log + '</div>' + \
           '<div>' + ibook_log + '</div>'
    msg = MIMEText(body, 'html')
    msg['subject'] = 'ifeng进度'
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
