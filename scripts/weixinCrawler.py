#coding=utf-8
import requests
import time
import codecs
from datetime import datetime
import pandas as pd
import csv
import re
import os
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def crawl_one_page(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'wxb_fp_id=2070419944; aliyungf_tc=AQAAAHfCQ3RFWw4ABLvHbxWddTlkOE0G; visit-wxb-id=2493b72ecf85c969396c1d20bd0c5ef0; wxb_fp_id=2070419944; PHPSESSID=fcb20ccc41de27850c7ccc7f21b1ac8f; Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91=1541840931,1541841249; Hm_lpvt_5859c7e2fd49a1739a0b0f5a28532d91=1541842574',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'data.wxb.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    res = requests.get(url=url, headers=headers)
    test = res

if __name__ == '__main__':
    crawl_one_page('https://data.wxb.com/details/postRead?id=gh_7418422c2a62')
