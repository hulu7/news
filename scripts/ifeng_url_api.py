#coding=utf-8
import requests
import utils
import time
from datetime import datetime
import csv
import re

def crawl_one_page(url_object, base_url):
    res = requests.get(url=url_object['url'])
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

def crawl_pages(base_url,class_name, restart):
    url_object_list = []
    saveCSVFilePath = '/home/dev/Repository_Test_Data/ifeng/' + restart['class'] + '.csv'
    csv_file = open(saveCSVFilePath, 'a')
    csv_writer = csv.writer(csv_file)
    if int(restart['i']) == 0 and int(restart['j']) == 0:
        csv_writer.writerow(['collect_time', 'id', 'title', 'class', 'url', 'docUrl', 'imageUrl', 'i_j_total'])
    for i in range(int(restart['i']), 100):
        for j in range(int(restart['j']), 100):
            url_object_list.append({
                'url': base_url + '/' + str(i) + '_' + str(j) + '/data.shtml',
                'i': str(i),
                'j': str(j)
            })

    for url_object in url_object_list:
        print url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name
        items = crawl_one_page(url_object, base_url)
        with open(saveTxtFilePath, 'w') as txt_writer:
            txt_writer.write(url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name)
        txt_writer.close()
        if items != None:
            for item in items:
                csv_writer.writerow([item['collect_time'], item['id'], item['title'], class_name, item['url'], item['docUrl'], item['imageUrl'], url_object['i'] + '_' + url_object['j'] + '_' + restart['total']])
                restart['total'] = str(int(restart['total']) + 1)
                with open(saveTxtFilePath, 'w') as txt_writer:
                    txt_writer.write(url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '_' + class_name)
                txt_writer.close()
                print url_object['i'] + '_' + url_object['j'] + '_' + restart['total'] + '---' + item['docUrl'] + '---' + item['title'] + '---' + class_name
        # time.sleep(2)
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
    for item in one_dic:
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
        if [item['name']] not in finished:
            if item['name'] == restart['class']:
                if int(restart['i']) < 99:
                    if int(restart['j']) < 99:
                        restart['j'] = str(int(restart['j']) + 1)
                    else:
                        restart['i'] = str(int(restart['i']) + 1)
                        restart['j'] = str(0)
                else:
                    if int(restart['j']) < 99:
                        restart['j'] = str(int(restart['j']) + 1)
                    else:
                        restart['i'] = str(0)
                        restart['j'] = str(0)
                        with open(saveTxtFilePath, 'w') as txt_writer:
                            txt_writer.write(
                                restart['i'] + '_' + restart['j'] + '_' + restart['total'] + '_' + restart['class'])
                        txt_writer.close()
                        with open(saveFinishedFilePath, 'a') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow([item['name']])
                        csv_file.close()
                        continue
            else:
                restart['class'] = item['name']
                restart['i'] = str(0)
                restart['j'] = str(0)
                with open(saveTxtFilePath, 'w') as txt_writer:
                    txt_writer.write(
                        restart['i'] + '_' + restart['j'] + '_' + restart['total'] + '_' + restart['class'])
                txt_writer.close()
            crawl_pages(item['href'], item['name'], restart)
            with open(saveFinishedFilePath, 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([item['name']])
            csv_file.close()
        else:
            continue

