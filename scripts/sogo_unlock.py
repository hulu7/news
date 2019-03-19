# encoding: utf-8
import requests
import time
import json
import hashlib

def getTime():
    current_time = time.time()
    time_seconds = str(current_time / 1e+9).replace('.', '') + '0'
    return time_seconds

def getSUV(time_seconds):
    m2 = hashlib.md5()
    m2.update(time_seconds)
    return m2.hexdigest()

def unlock(antiurl, oldcookies):
    retries = 0
    while retries < 3:
        r = requests
        tc = int(round(time.time() * 1000))
        captcha = r.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={0}'.format(tc), cookies=oldcookies)

        with open('captcha.jpg', 'wb') as file:
            file.write(captcha.content)

        c = input("请输入captcha.jpg中的验证码:")

        thank_url = 'http://weixin.sogou.com/antispider/thank.php'
        formdata = {
            'c': c,
            'r': '%2F' + antiurl,
            'v': 5
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + antiurl
        }

        resp = r.post(thank_url, data=formdata, headers=headers, cookies=oldcookies)

        resp = json.loads(resp.text)

        if resp.get('code') != 0:
            print ("解锁失败。重试次数:{0:d}".format(3 - retries))
            retries += 1
            continue

        oldcookies['SNUID'] = resp.get('id')
        oldcookies['SUV'] = '00D80B85458CAE4B5B299A407EA3A580'
        # print ("更新Cookies。", oldcookies)

        return oldcookies


b = unlock("https://weixin.sogou.com/antispider/?from=%2fweixin%3Ftype%3d1%26s_from%3dinput%26query%3d%E9%82%BB%E7%AB%A0%26ie%3dutf8%26_sug_%3dn%26_sug_type_%3d", )
print b