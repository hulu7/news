#coding=utf-8
import sys
sys.path.append("..")
from common.ifengUrlCrawler import ifengUrlCrawler

if __name__ == '__main__':
    item = {'href' : 'http://inews.ifeng.com', 'name' : '新闻'}
    basePath = '/home/dev/Repository_Test_Data/ifeng'
    max_deep = 100
    urlSpider = ifengUrlCrawler()
    urlSpider.startIfengUrlSpider(item, basePath, max_deep)