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
    base_path2 = '//home//dev//Backups//spiderNode1//files//ifeng//log//'

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

    ient_file2=open(base_path2 + 'ient//cache.txt', 'r')
    ient_log2=ient_file2.read()
    ient_file2.close()

    ifashion_file2=open(base_path2 + 'ifashion//cache.txt', 'r')
    ifashion_log2=ifashion_file2.read()
    ifashion_file2.close()

    ifinance_file2=open(base_path2 + 'ifinance//cache.txt', 'r')
    ifinance_log2=ifinance_file2.read()
    ifinance_file2.close()

    ihistory_file2=open(base_path2 + 'ihistory//cache.txt', 'r')
    ihistory_log2=ihistory_file2.read()
    ihistory_file2.close()

    imil_file2=open(base_path2 + 'imil//cache.txt', 'r')
    imil_log2=imil_file2.read()
    imil_file2.close()

    inews_file2=open(base_path2 + 'inews//cache.txt', 'r')
    inews_log2=inews_file2.read()
    inews_file2.close()

    isports_file2=open(base_path2 + 'isports//cache.txt', 'r')
    isports_log2=isports_file2.read()
    isports_file2.close()

    itech_file2=open(base_path2 + 'itech//cache.txt', 'r')
    itech_log2=itech_file2.read()
    itech_file2.close()

    iculture_file2=open(base_path2 + 'iculture//cache.txt', 'r')
    iculture_log2=iculture_file2.read()
    iculture_file2.close()

    ibook_file2=open(base_path2 + 'ibook//cache.txt', 'r')
    ibook_log2=ibook_file2.read()
    ibook_file2.close()

    body = '<div>------------Dev------------</div>' + \
           '<p>娱乐:</p>' + '<p>'+ ient_log +'</p>' + \
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
           '<div></div>' + \
           '<p>文化:</p>' + '<p>' + iculture_log + '</p>' + \
           '<div></div>' + \
           '<p>读书:</p>' + '<p>' + ibook_log + '</p>' + \
           '<div>------------SpiderNode1------------</div>' + \
           '<p>娱乐:</p>' + '<p>' + ient_log2 + '</p>' + \
           '<div></div>' + \
           '<p>时尚:</p>' + '<p>' + ifashion_log2 + '</p>' + \
           '<div></div>' + \
           '<p>金融:</p>' + '<p>' + ifinance_log2 + '</p>' + \
           '<div></div>' + \
           '<p>历史:</p>' + '<p>' + ihistory_log2 + '</p>' + \
           '<div></div>' + \
           '<p>军事:</p>' + '<p>' + imil_log2 + '</p>' + \
           '<div></div>' + \
           '<p>新闻:</p>' + '<p>' + inews_log2 + '</p>' + \
           '<div></div>' + \
           '<p>体育:</p>' + '<p>' + isports_log2 + '</p>' + \
           '<div></div>' + \
           '<p>科技:</p>' + '<p>' + itech_log2 + '</p>' + \
           '<div></div>' + \
           '<p>文化:</p>' + '<p>' + iculture_log2 + '</p>' + \
           '<div></div>' + \
           '<p>读书:</p>' + '<p>' + ibook_log2 + '</p>' + \
           '<div></div>'
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
