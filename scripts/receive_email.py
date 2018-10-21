# -*- coding: utf-8 -*-
import imaplib
import email
import sys
reload(sys)
sys.setdefaultencoding('gbk')

def saveFile(file_name, data, path):
    try:
        file_path = path + file_name
        print 'Saved as ' + file_path
        file = open(file_path, 'wb')
    except:
        print('file name error')
        file.close()
    file.write(data)
    file.close()

def myUnicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)

def getCharset(message, default="ascii"):
    return message.getCharset()
    return default

def parseEmail(msg, my_path):
    mail_content = None
    content_type = None
    suffix =None
    for part in msg.walk():
        if not part.is_multipart():
            content_type = part.get_content_type()
            filename = part.get_filename()
            charset = getCharset(part)
            if filename:
                h = email.Header.Header(filename)
                dh = email.Header.decode_header(h)
                fname = dh[0][0]
                encodeStr = dh[0][1]
                if encodeStr != None:
                    if charset == None:
                        fname = fname.decode(encodeStr, 'gbk')
                    else:
                        fname = fname.decode(encodeStr, charset)
                data = part.get_payload(decode=True)
                print('Attachment : ' + fname)
                if fname != None or fname != '':
                    saveFile(fname, data, my_path)
            else:
                if content_type in ['text/plain']:
                    suffix = '.txt'
                if content_type in ['text/html']:
                    suffix = '.htm'
                if charset == None:
                    mail_content = part.get_payload(decode=True)
                else:
                    mail_content = part.get_payload(decode=True).decode(charset)
    return  (mail_content, suffix)


def getMail(mail_host, account, password, disk_root, port=465, ssl=1):
    my_path = disk_root + ':\\'
    if ssl == 1:
        imap_server = imaplib.IMAP4_SSL(mail_host, port)
    else:
        imap_server = imaplib.IMAP4(mail_host, port)
    imap_server.login(account, password)
    imap_server.select()
    resp, items = imap_server.search(None, "Unseen")
    number = 1
    for i in items[0].split():
        # get information of email
        resp, mail_data = imap_server.fetch(i, "(RFC822)")
        mail_text = mail_data[0][1]
        msg = email.message_from_string(mail_text)
        ls = msg["From"].split(' ')
        str_from = ''
        if (len(ls) == 2):
            from_name = email.Header.decode_header((ls[0]).strip('\"'))
            str_from = 'From : ' + myUnicode(from_name[0][0], from_name[0][1]) + ls[1]
        else:
            str_from = 'From : ' + msg["From"]
        str_date = 'Date : ' + msg["Date"]
        subject = email.Header.decode_header(msg["Subject"])
        sub = myUnicode(subject[0][0], subject[0][1])
        str_sub = 'Subject : ' + sub

        mail_content, suffix = parseEmail(msg, my_path)
        # 命令窗体输出邮件基本信息
        print '\n'
        print 'No : ' + str(number)
        print str_from
        print str_date
        print str_sub
        '''
        print 'Content:'
        print mailContent
        '''
        # 保存邮件正文
        if (suffix != None and suffix != '') and (mail_content != None and mail_content != ''):
            saveFile(str(number) + suffix, mail_content, my_path)
            number = number + 1

    imap_server.close()
    imap_server.logout()

if __name__ =="__main__":
    #邮件保存在e盘
    mypath ='/home/Email/'
    print 'begin to get email...'
    # getMail('pop.gmail.com', 'xxxxxxxx@gmail.com', 'xxxxxxxx', mypath, 993, 1)
    #126邮箱登陆没用ssl
    getMail('imap.qq.com', 'huiskai@qq.com', 'thebestornothing', mypath, 465, 0)
    print 'the end of get email.'