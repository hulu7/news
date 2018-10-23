#coding=utf-8
import requests
import utils
import time
from datetime import datetime
import csv
import re

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
        with open(saveTxtFilePath, 'w') as txt_writer:
            txt_writer.write(url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name)
        txt_writer.close()
        items = crawl_one_page(url_object, base_url)

        time.sleep(1)
        if items != None:
            for item in items:
                csv_writer.writerow([item['collect_time'], item['id'], item['title'], class_name, item['url'], item['docUrl'], item['imageUrl'], url_object['i'] + '_' + url_object['j'] + '_' + restart['total']])
                restart['total'] = str(int(restart['total']) + 1)
                with open(saveTxtFilePath, 'w') as txt_writer:
                    txt_writer.write(url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name)
                txt_writer.close()
                print url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '---' + item['docUrl'] + '---' + item['title'] + '---' + class_name
    csv_file.close()

if __name__ == '__main__':
    one_dic = [{'href' : 'http://inews.ifeng.com',
                    'name' : '新闻'},
                {'href': 'http://ifinance.ifeng.com',
                    'name': '财经'},
                {'href' : 'http://ient.ifeng.com',
                    'name' : '娱乐'},
                {'href' : 'http://isports.ifeng.com',
                    'name' : '体育'},
                {'href' : 'http://imil.ifeng.com',
                    'name' : '军事'},
                {'href':  'http://auto.ifeng.com/',
                    'name':'汽车'},
                {'href' : 'http://ifashion.ifeng.com',
                    'name' : '时尚'},
                {'href' : 'http://itech.ifeng.com',
                    'name' : '科技'},
                {'href' : 'http://ihistory.ifeng.com',
                    'name' : '历史'},
                {'href':  'http://g.ifeng.com/',
                                'name':  '游戏'}
    ]

    saveTxtFilePath = '/home/dev/Repository/news/scripts/deep_cache.txt'
    saveFinishedFilePath = '/home/dev/Repository/news/scripts/deep_cache_finished.csv'
    restart = {
        'i': '0',
        'j': '0',
        'total': '0',
        'class': ''
    }
    finished = []
    with open(saveFinishedFilePath, 'r') as scv_file:
        finished = list(csv.reader(scv_file))
    scv_file.close()

    with open(saveTxtFilePath, 'r') as txt_file:
        result = re.split('_', txt_file.read().strip('\n'))
        restart['i'] = str(result[0])
        restart['j'] = str(result[1])
        restart['total'] = str(result[2])
        restart['class'] = str(result[3])
    txt_file.close()
    for item in one_dic:
        if int(restart['i']) == 99 and int(restart['j']) == 99:
            restart['i'] = str(0)
            restart['j'] = str(0)
            csv_file = open(saveFinishedFilePath, 'a')
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([restart['class']])
            restart['class'] = item['name']
        if [item['name']] not in finished:
            url_object_list = []
            saveCSVFilePath = '/home/dev/Repository_Test_Data/ifeng/' + restart['class'] + '.csv'
            csv_file = open(saveCSVFilePath, 'a')
            csv_writer = csv.writer(csv_file)
            if int(restart['i']) == 0 and int(restart['j']) == 0:
                csv_writer.writerow(
                    ['collect_time', 'id', 'title', 'class', 'url', 'docUrl', 'imageUrl', 'i_j_total'])
            for i in range(int(restart['i']), 100):
                if i == int(restart['i']):
                    j_restart = int(restart['j'])
                else:
                    j_restart = 0
                for j in range(j_restart, 100):
                    url_object_list.append({
                        'url': item['href'] + '/' + str(i) + '_' + str(j) + '/data.shtml',
                        'i': str(i),
                        'j': str(j)
                    })
            crawl_pages(url_object_list, item['href'],item['name'], restart)
        else:
            continue

