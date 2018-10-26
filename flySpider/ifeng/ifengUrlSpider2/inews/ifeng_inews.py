#coding=utf-8
import requests
import utils
import time
from datetime import datetime
import csv
import re
import os

def crawl_one_page(url_object, base_url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Connection': 'keep-alive',
        'Cookie': '__gads=ID=adf05843f7a8c25a:T=1516456065:S=ALNI_MYdyId0LTBNnR1jsNjtWActIo293Q; userid=1516456066445_i814dz7888; vjuids=fd54fddaf.1615f790f1f.0.1a2acdc58b146; cookieBloone=false; UM_distinctid=16547e444075bd-0c4b7f15f665d5-3c60460e-144000-16547e4440878f; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI1YmI5YjM3ZjE4ZDYzIiwidGltZSI6MTUzODg5Njc2N30.x9TjQ2PlvQXuTZC3unuAsA8UF-ysMleKpyOmD5kaRXI; vjlast=1517725225.1539408123.23; city=010; weather_city=bj; prov_ifeng=cn010; if_mid=1516456066445_i814dz7888; region_ip=111.199.188.x; region_ver=1.2',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Host': re.split('//', base_url)[1],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    res = requests.get(url=url_object['url'], headers=headers)
    if res.status_code != 200:
        print 'time out occure'
        time.sleep(60)
        return None
    str = res.text.encode('utf-8')
    if str=='getListDatacallback([]);' or str=='getListDatacallback({});' or str == 'getListDatacallback(出现异常);':
        return None
    str_n = str[str.find('(') + 1:-2]
    str_n = str_n.replace('null', 'None')
    dics = eval(str_n)
    items = []
    for one in dics:
        item = {}
        item['title'] = utils.part_ustr_to_str(one['title'])
        page_url = one['pageUrl']
        item['url'] = base_url+page_url
        item['docUrl'] = one['docUrl']
        item['imageUrl'] = one['i_thumbnail']
        item['collect_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['id'] = page_url[page_url.find('/')+1:page_url.find('/n')]
        items.append(item)
    return items

def crawl_pages(url_object_list, base_url,class_name, restart):
    if len(url_object_list) == 0:
        return
    for url_object in url_object_list:
        print url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name
        writeToTxt(cacheFilePath, url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name)
        items = crawl_one_page(url_object, base_url)

        if items != None:
            for item in items:
                finishedIds = readFromCSV(finishedIdPath)
                if [item['id']] not in finishedIds:
                    writeToCSV(saveCSVFilePath, [item['collect_time'], item['id'], item['title'], class_name, item['url'], item['docUrl'], item['imageUrl'], url_object['i'] + '_' + url_object['j'] + '_' + restart['total']])
                    writeToCSV(finishedIdPath, [item['id']])
                    restart['total'] = str(int(restart['total']) + 1)
                    writeToTxt(cacheFilePath, url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name)
                    print url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '---' + item['docUrl'] + '---' + item['title'] + '---' + class_name

def writeToCSV(file_path, content):
    with open(file_path, 'a') as scv_file:
        csv_writer = csv.writer(scv_file)
        csv_writer.writerow(content)
    scv_file.close()

def readFromCSV(file_path):
    content = []
    with open(file_path, 'r') as scv_file:
        content = list(csv.reader(scv_file))
    scv_file.close()
    return content

def readFromTxt(file_path):
    with open(file_path, 'r') as txt_file:
        content = txt_file.read()
    txt_file.close()
    return content

def writeToTxt(file_path, content):
    with open(file_path, 'w') as txt_writer:
        txt_writer.write(content)
    txt_writer.close()

def readCacheInfo(file_path):
    cache = re.split('_', readFromTxt(file_path).strip('\n'))
    restart['i'] = str(cache[0])
    restart['j'] = str(cache[1])
    restart['total'] = str(cache[2])
    restart['class'] = str(cache[3])
    return restart

if __name__ == '__main__':
    item = {'href' : 'http://inews.ifeng.com', 'name' : '新闻'}
    max_deep = 100
    cacheFilePath = '/home/dev/Repository_Test_Data/ifeng/log/inews/cache.txt'
    finishedIdPath = '/home/dev/Repository_Test_Data/ifeng/log/inews/finished_id.csv'

    restart = {
        'i': '0',
        'j': '0',
        'total': '0',
        'class': ''
    }

    finishedIds = []

    isCacheFileExits = os.path.exists(cacheFilePath)
    if isCacheFileExits:
       restart = readCacheInfo(cacheFilePath)
    else:
        writeToTxt(cacheFilePath, '0_0_0_' + item['name'])

    isFinishedIdFileExits = os.path.exists(finishedIdPath)
    if isFinishedIdFileExits:
        finishedIds = readFromCSV(finishedIdPath)
    else:
        writeToCSV(finishedIdPath, ['Finished'])

    restart = readCacheInfo(cacheFilePath)
    if int(restart['i']) == (max_deep - 1) and int(restart['j']) == (max_deep - 1):
        restart['i'] = str(0)
        restart['j'] = str(0)

    url_object_list = []
    saveCSVFilePath = '/home/dev/Repository_Test_Data/ifeng/' + item['name'] + '.csv'
    saveFileExits = os.path.exists(saveCSVFilePath)
    if saveFileExits is False:
        writeToCSV(saveCSVFilePath, ['collect_time', 'id', 'title', 'class', 'url', 'docUrl', 'imageUrl', 'i_j_total'])

    for i in range(int(restart['i']), max_deep):
        if i == int(restart['i']):
            j_restart = int(restart['j'])
        else:
            j_restart = 0
        for j in range(j_restart, max_deep):
            url_object_list.append({
                'url': item['href'] + '/' + str(i) + '_' + str(j) + '/data.shtml',
                'i': str(i),
                'j': str(j)
            })
    crawl_pages(url_object_list, item['href'], item['name'], restart)
