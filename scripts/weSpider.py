#coding=utf-8
import requests
import utils
import time
from datetime import datetime
from lxml import etree
import csv
import re
import os
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WeiXinSpider():

    def writeToCSV(self, file_path, content):
        with open(file_path, 'a') as scv_file:
            csv_writer = csv.writer(scv_file)
            csv_writer.writerow(content)
        scv_file.close()

    def readFromCSV(self, file_path):
        content = []
        with open(file_path, 'r') as scv_file:
            content = list(csv.reader(scv_file))
        scv_file.close()
        return content

    def readFromTxt(self, file_path):
        with open(file_path, 'r') as txt_file:
            content = txt_file.read()
        txt_file.close()
        return content

    def writeToTxt(self, file_path, content):
        with open(file_path, 'w') as txt_writer:
            txt_writer.write(content)
        txt_writer.close()

    def readCacheInfo(self, file_path):
        restart = {}
        cache = re.split('_', self.readFromTxt(file_path).strip('\n'))
        restart['i'] = str(cache[0])
        restart['j'] = str(cache[1])
        restart['total'] = str(cache[2])
        restart['class'] = str(cache[3])
        return restart

    def writeToMongo(self, content):
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019', replicaset='repset')

        db = client[self.domain]
        mongodbItem = dict(content)
        db.contentInfo.insert(mongodbItem)
        client.close()

    def getTime(self):
        currentTime = time.time()
        timeNumber = str(currentTime / 1e+9).replace('.', '') + '0'
        return timeNumber

    def createRequestUrl(self, id):
        t = self.getTime()
        url = 'https://weixin.sogou.com/weixinwap?ie=utf8&s_from=input&type=2&t=' + t + '&pg=webSearchList&_sug_=n&_sug_type_=&query=' + id
        return url

    def createRequestHeaders(self, requestUrl):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'pgv_pvi=5890523136; tvfe_boss_uuid=13616fb7559cdc17; pgv_pvid=4278477681; RK=MA+C6STKND; ptcz=cd0e6878d3613658422107def96c91a6dbfa7ea523a23540cea0debd2a75cd2c; ptui_loginuin=huiskai@qq.com; mm_lang=zh_CN; o_cookie=1296297596; pac_uid=1_1296297596; pt2gguin=o0838005159; rewardsn=; wxtokenkey=777; sig=h01ac12e96ebacad9874509a7dc0dbcb82e5b6e74c77ea953740d8ede150d52aa4c1eb9dea1c922e77d',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'mp.weixin.qq.com',
            'Referer': requestUrl,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        return headers

    def startSearch(self, url):
        headers = self.createRequestHeaders(url)
        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            print 'time out occure'
            time.sleep(10)
            return None
        urls = self.startParse(response)
        return urls

    def startParse(self, response):
        if len(response.content) == 0:
            return
        html = response.content
        selector = etree.HTML(html)
        urls = selector.xpath('//h4[@class="weui_media_title"]/@href')
        return urls


    def startSpider(self, gz_list):
        if len(gz_list) == 0:
            return
        urls = []
        for item in gz_list:
            urls.append(self.startSearch(item['href']))
        return urls

if __name__ == '__main__':
    gz_list = [{'href' : 'http://mp.weixin.qq.com/profile?src=3&timestamp=1542284554&ver=1&signature=D1z5hwr9SQQdbJ4mhi3ZmJAIoEHNnO4seZ6F02GuWIJ0fxnqi3d3xlXppph0xLN5nP5I4RY3timcr3U6sBPoVQ=='},
               {'href': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1542287289&ver=1&signature=ljFJfnheo9W0Shm9sIyLCnoi6R-E8eXjHiKlYaVYTRO0ngmz*kpVVtrGlEuAgk-E7lF0WvY1DNS6-C9Sg7px2w=='},
               {'href': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1542287318&ver=1&signature=aXO5WqSr04wwD4WFBwFJzUSIKyMsvPGHg20-yTl5xdt1ZLve0CP4i18RJTeOIw-f7ToqaGItnM8G4NKQtTCj1w=='},
               {'href': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1542287340&ver=1&signature=fOENhBUrEM6XcuNRY3ue306JhgArSpPZiBMBVjqYHd82S9AhKAcqj1ZZOkNSUmec36YMuc9Dt6FKLAY8dSUmuw=='}]
    weixinSpider = WeiXinSpider()
    weixinSpider.startSpider(gz_list)
