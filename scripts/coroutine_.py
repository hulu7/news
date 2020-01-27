# -*- coding: utf-8 -*-
#------requirement------
#gevent-1.3.7
#selenium-3.14.1
#Scrapy-1.5.1
#
#
#------requirement------
from selenium import webdriver
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def __init__(executable_path=None):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    return browser

def run_task(url):
    browser = __init__(executable_path='/usr/bin/chromedriver')
    print 'Visit --> %s' %url
    try:
        browser.get(url)
        response = browser.page_source
        html = etree.HTML(response)
        title = html.xpath(".//*[contains(@class,'yc_tit')]/h1/text()")
        # html = etree.parse(response)
        # article_0 = response.xpath(".//*[@id='artical']")
        # article_1 = response.xpath(".//*[contains(@class,'yc_main wrap')]")
        # if len(article_0.extract()) > 0:
        #     article = article_0
        #     comment_number = filter(str.isdigit,article.xpath(".//*[contains(@class,'js_cmtNum')]").xpath('string(.)').extract()[0].encode('gbk'))
        #     join_number = filter(str.isdigit,article.xpath(".//*[contains(@class,'js_joinNum')]").xpath('string(.)').extract()[0].encode('gbk'))
        #     url = response.url
        #     content = article.xpath(".//div[@id='main_content']").xpath('string(.)').extract()[0].strip()
        #     time = article.xpath(".//*[contains(@class,'ss01')]").xpath('string(.)').extract()[0].strip()
        #     author_name = article.xpath(".//*[contains(@class,'ss03')]").xpath('string(.)').extract()[0]
        #     title = article.xpath(".//*[@id='artical_topic']").xpath('string(.)').extract()[0].strip()
        print title[0].encode('utf8')
        browser.close()
    except Exception as e:
        print e.message
    return 'url:%s ---> finished' % url

if __name__ == '__main__':
    pool = Pool(2)
    # urls = ['https://www.huxiu.com', 'http://www.ifeng.com/', 'http://www.ce.cn/']
    urls = ['http://news.ifeng.com/a/20181121/60169573_0.shtml']
    result = pool.map(run_task, urls)
    print result