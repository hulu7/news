# -*- coding: utf-8 -*-
#------requirement------
#gevent-1.3.7
#selenium-3.14.1
#Scrapy-1.5.1
#
#
#------requirement------
from selenium import webdriver
from multiprocessing import Pool
import os, time

def init(executable_path=None):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    return browser

def run_task(url):
    browser = init(executable_path='/usr/bin/chromedriver')
    print 'Task %s (pid = %s) is running ...' % (url, os.getpid())
    browser.get(url)
    response = browser.page_source
    time.sleep(1)
    print 'Task %s end.' % url

if __name__ == '__main__':
    print 'Current process %s.' % os.getpid()
    p = Pool(processes=3)
    # urls = ['https://github.com', 'https://www.huxiu.com', 'https://www.baidu.com']
    urls = ['http://news.ifeng.com/a/20181122/60170977_0.shtml', 'http://news.ifeng.com/a/20181121/60169573_0.shtml']
    for url in urls:
        p.apply_async(run_task, args=(url,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocess done.'