# -*- coding: utf-8 -*-
import smtplib
import email.MIMEMultipart  # import MIMEMultipart
import email.MIMEText  # import MIMEText
import email.MIMEBase  # import MIMEBase
from email.mime.application import MIMEApplication
import os.path

From = "zixun18@163.com"
To = "huiskai@qq.com"
file_base_path = r"/home/dev/Data/files/huxiu/txt/"

server = smtplib.SMTP("smtp.163.com")
server.login("zixun18@163.com", "thebest1990")

main_msg = email.MIMEMultipart.MIMEMultipart()
part = email.MIMEText.MIMEText("这是所有文章，请您查收", _charset="utf-8")
main_msg.attach(part)

contype = 'application/octet-stream'
maintype, subtype = contype.split('/', 1)

cacheFilePath = '/home/dev/Repository/news/scripts/send_email_cache.txt'
with open(cacheFilePath, 'r') as txt_file:
    last_sent = int(txt_file.read().strip('\n'))
txt_file.close()
files = os.listdir(file_base_path)
for index in range(last_sent, last_sent + 10):
    file_name = files[index]
    part = MIMEApplication(open(file_base_path + file_name, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=file_name)
    main_msg.attach(part)
    last_sent = index + 1

main_msg['From'] = From
main_msg['To'] = To
main_msg['Subject'] = "第" + str(last_sent - 10) + ' - ' + str(last_sent) + '篇文章'
main_msg['Date'] = email.Utils.formatdate()

fullText = main_msg.as_string()

try:
    server.sendmail(From, To, fullText)
    with open(cacheFilePath, 'w') as txt_writer:
        txt_writer.write(str(last_sent))
    txt_writer.close()
    print ('Done.sent email success')
except smtplib.SMTPException:
    print ('Error.sent email fail')
finally:
    server.quit()