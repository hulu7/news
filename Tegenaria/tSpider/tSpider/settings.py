# -*- coding: utf-8 -*-
import time
class Settings():

    SELENIUM_TIMEOUT = 300
    CHROMEDRIVER_PATH = "//usr//bin//chromedriver"

    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9,en;q=0.8"
    ACCEPT_ENC0DING = "gzip, deflate"
    CONNECTION = "keep-alive"
    CACHE_CONTROL = "max-age=0"
    PRAGMA = "no-cache"
    UPGRADE_INSECURE_REQUESTS = "1"

    RSYNC_PRD1 = "//home//dev//Data//rsyncData//prd4"
    RSYNC_PRD2 = "//home//dev//Data//rsyncData//prd3"

    CAMEL_FOOD = "//home//dev//Repository//news//Tegenaria//tSpider//tSpider//food"

    LOG_PATH = "{0}//log".format(RSYNC_PRD1)
    LOG_PATH_PRD2 = "{0}//log".format(RSYNC_PRD2)

    MONGO_URI = 'mongodb://127.0.0.1:27017'

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    BLOOMFILTER_NAME = "tegenaria:dupefilter"

    TODAY = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    CHRONUS_SETTINGS = "{0}//log//chronus.csv".format(RSYNC_PRD1)

    DISABLE_RESTART_INTERVAL = False

    SETTINGS_HUXIU = 'huxiu'
    HUXIU = {
        'NAME': SETTINGS_HUXIU,
        'MONGO': SETTINGS_HUXIU,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_HUXIU),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_HUXIU, SETTINGS_HUXIU),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_HUXIU, SETTINGS_HUXIU),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_HUXIU),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_CE = 'ce'
    CE = {
        'NAME': SETTINGS_CE,
        'MONGO': SETTINGS_CE,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_CE),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_CE),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_CE),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_CE),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_CE),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_CE, SETTINGS_CE),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_CE, SETTINGS_CE),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_CE),
        'RESTART_INTERVAL': 20,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_CE),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_EEO = 'eeo'
    EEO = {
        'NAME': SETTINGS_EEO,
        'MONGO': SETTINGS_EEO,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_EEO),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_EEO),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_EEO),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_EEO),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_EEO, SETTINGS_EEO),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_EEO, SETTINGS_EEO),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_EEO),
        'RESTART_INTERVAL': 120,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_EEO),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_HUANQIU = 'huanqiu'
    HUANQIU = {
        'NAME': SETTINGS_HUANQIU,
        'MONGO': SETTINGS_HUANQIU,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_HUANQIU),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_HUANQIU),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_HUANQIU),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_HUANQIU),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_HUANQIU, SETTINGS_HUANQIU),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_HUANQIU, SETTINGS_HUANQIU),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_HUANQIU),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_HUANQIU),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_CANKAOXIAOXI = 'cankaoxiaoxi'
    CANKAOXIAOXI = {
        'NAME': SETTINGS_CANKAOXIAOXI,
        'MONGO': SETTINGS_CANKAOXIAOXI,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_CANKAOXIAOXI),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI, SETTINGS_CANKAOXIAOXI),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI, SETTINGS_CANKAOXIAOXI),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI),
        'RESTART_INTERVAL': 10,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_CANKAOXIAOXI),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_GUANCHA = 'guancha'
    GUANCHA = {
        'NAME': SETTINGS_GUANCHA,
        'MONGO': SETTINGS_GUANCHA,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_GUANCHA),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_GUANCHA),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_GUANCHA),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_GUANCHA),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_GUANCHA, SETTINGS_GUANCHA),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_GUANCHA, SETTINGS_GUANCHA),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_GUANCHA),
        'RESTART_INTERVAL': 5,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_GUANCHA),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_YICAI = 'yicai'
    YICAI = {
        'NAME': SETTINGS_YICAI,
        'MONGO': SETTINGS_YICAI,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_YICAI),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_YICAI),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_YICAI),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_YICAI),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_YICAI, SETTINGS_YICAI),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_YICAI, SETTINGS_YICAI),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_YICAI),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_YICAI),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_IFENG = 'ifeng'
    IFENG = {
        'NAME': SETTINGS_IFENG,
        'MONGO': SETTINGS_IFENG,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_IFENG),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_IFENG),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_IFENG),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_IFENG),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_IFENG, SETTINGS_IFENG),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_IFENG, SETTINGS_IFENG),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_IFENG),
        'RESTART_INTERVAL': 5,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_IFENG),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_JINGJI21 = 'jingji21'
    JINGJI21 = {
        'NAME': SETTINGS_JINGJI21,
        'MONGO': SETTINGS_JINGJI21,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_JINGJI21),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_JINGJI21, SETTINGS_JINGJI21),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_JINGJI21, SETTINGS_JINGJI21),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_JINGJI21),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_STCN = 'stcn'
    STCN = {
        'NAME': SETTINGS_STCN,
        'MONGO': SETTINGS_STCN,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_STCN),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_STCN),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_STCN),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_STCN),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_STCN, SETTINGS_STCN),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_STCN, SETTINGS_STCN),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_STCN),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_STCN),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_WALLSTREETCN = 'wallstreetcn'
    WALLSTREETCN = {
        'NAME': SETTINGS_WALLSTREETCN,
        'MONGO': SETTINGS_WALLSTREETCN,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_WALLSTREETCN),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_WALLSTREETCN),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_WALLSTREETCN),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_WALLSTREETCN),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_WALLSTREETCN),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_WALLSTREETCN, SETTINGS_WALLSTREETCN),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_WALLSTREETCN, SETTINGS_WALLSTREETCN),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_WALLSTREETCN),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_WALLSTREETCN),
        'IS_OPEN_CACHE': False
    }

    SETTINGS_CHUANSONGME = 'chuansongme'
    CHUANSONGME = {
        'NAME': SETTINGS_CHUANSONGME,
        'MONGO': SETTINGS_CHUANSONGME,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_CHUANSONGME),
        'FINISHED_IDS': "{0}_finished_ids".format(SETTINGS_CHUANSONGME),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_CHUANSONGME),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_CHUANSONGME),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_CHUANSONGME),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_CHUANSONGME, SETTINGS_CHUANSONGME),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_CHUANSONGME, SETTINGS_CHUANSONGME),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_CHUANSONGME),
        'RESTART_INTERVAL': 120,
        'MAX_POOL_SIZE': 5,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_CHUANSONGME),
        'IS_OPEN_CACHE': True
    }

    SETTINGS_I36KR = '36kr'
    I36KR = {
        'NAME': SETTINGS_I36KR,
        'MONGO': SETTINGS_I36KR,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_I36KR),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_I36KR),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_I36KR),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_I36KR),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_I36KR),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_I36KR, SETTINGS_I36KR),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_I36KR, SETTINGS_I36KR),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_I36KR),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': "{0}//{1}.txt".format(CAMEL_FOOD, SETTINGS_I36KR),
        'IS_OPEN_CACHE': False
    }

