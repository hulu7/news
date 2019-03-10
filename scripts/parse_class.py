#coding=utf-8
import requests
import csv
import re
from lxml import etree
import os
from bs4 import BeautifulSoup

def crawl_one_page(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cookie': '__gads=ID=adf05843f7a8c25a:T=1516456065:S=ALNI_MYdyId0LTBNnR1jsNjtWActIo293Q; userid=1516456066445_i814dz7888; vjuids=fd54fddaf.1615f790f1f.0.1a2acdc58b146; cookieBloone=false; Hm_lvt_eec74a48e4ee616a7d04ec5386b2110a=1528033289; UM_distinctid=16547e444075bd-0c4b7f15f665d5-3c60460e-144000-16547e4440878f; TEMP_USER_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI1YmI5YjM3ZjE4ZDYzIiwidGltZSI6MTUzODg5Njc2N30.x9TjQ2PlvQXuTZC3unuAsA8UF-ysMleKpyOmD5kaRXI; CNZZDATA5305352=cnzz_eid%3D350468294-1524757203-http%253A%252F%252Fwww.ifeng.com%252F%26ntime%3D1539777778; city=010; weather_city=bj; prov_ifeng=cn010; if_mid=1516456066445_i814dz7888; prov=cn010; region_ip=111.199.189.235; region_ver=1.30; vjlast=1517725225.1540657918.11',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://chuansongme.com/n/2842241949523',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        print 'status: ' + response.status_code
        return None
    response.encoding = 'gb18030'
    response = response.text
    soup = BeautifulSoup(response, 'html.parser')
    item_list = soup.find_all('div', class_=['col3', 'col4'])
    for item in item_list:
        nav_list = []
        h2 = item.find('h2')
        title_parent = h2.string.encode('gb18030')
        url_parent = h2.find('a').get('href')
        for filter in ['col_nav', 'col_banner', 'clearfix', 'col_b1000', 'box_nav', 'mainMenu', 'list1', 'list2', 'nav', 'area_nav']:
            nav_parent = item.find('div', class_=filter)
            if nav_parent != None:
                nav_list = nav_list + nav_parent.find_all('a')

        for nav_item in nav_list:
            if nav_item.string != None:
                title_child = nav_item.string.encode('gb18030')
            else:
                title_child = ""
            url_child = nav_item.get('href')
            writeToCSV(saveFilePath, [title_parent, url_parent, title_child, url_child])


def crawl_pages(url):
    if len(url) == 0:
        return
    crawl_one_page(url)

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

if __name__ == '__main__':
    url = 'https://chuansongme.com/n/2842241949523'
    saveFilePath = '/home/dev/Data/test.csv'

    isSaveFileExits = os.path.exists(saveFilePath)
    if isSaveFileExits:
       restart = readFromCSV(saveFilePath)
    else:
        writeToCSV(saveFilePath, ['parent', 'url', 'child', 'url'])

    crawl_pages(url)
