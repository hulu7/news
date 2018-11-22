#coding=utf-8
import sys
sys.path.append("..")
from common.ifengUrlCrawler import ifengUrlCrawler

if __name__ == '__main__':
    item = {'href' : 'http://isports.ifeng.com', 'name' : '体育'}
    basePath = '/home/dev/Data'
    max_deep = 100
    urlSpider = ifengUrlCrawler()
    urlSpider.startIfengUrlSpider(item, basePath, max_deep)
