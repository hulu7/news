# -*- coding: utf-8 -*-

class Settings():

    SELENIUM_TIMEOUT = 120
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

    RSYNC_PRD1 = "//home//dev//Data//rsyncData//prd4"
    RSYNC_PRD2 = "//home//dev//Data//rsyncData//prd3"

    LOG_PATH = "{0}//log".format(RSYNC_PRD1)
    LOG_PATH_PRD2 = "{0}//log".format(RSYNC_PRD2)

    MONGO_URI = 'mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019'
    REPLICASET = 'repset'

    CHRONUS_SETTINGS = "{0}//log//chronus.csv".format(RSYNC_PRD1)

    SETTINGS_HUXIU = 'huxiu'
    HUXIU = {
        'NAME': SETTINGS_HUXIU,
        'MONGO': SETTINGS_HUXIU,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_HUXIU),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_HUXIU, SETTINGS_HUXIU),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_HUXIU, SETTINGS_HUXIU),
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://www.huxiu.com/']
    }

    SETTINGS_SP = 'sp'
    SP = {
        'NAME': SETTINGS_SP,
        'MONGO': SETTINGS_SP,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_SP),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_SP),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_SP),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_SP),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_SP),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_SP),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_SP, SETTINGS_SP),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_SP, SETTINGS_SP),
        'MAX_POOL_SIZE': 2,
        'URLS':['http://www.bjhd.gov.cn/xinxigongkai/zdly/zf/']
    }

    SETTINGS_CE = 'ce'
    CE = {
        'NAME': SETTINGS_CE,
        'MONGO': SETTINGS_CE,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_CE),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_CE),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_CE),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_CE),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_CE),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_CE),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_CE, SETTINGS_CE),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_CE, SETTINGS_CE),
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://www.ce.cn/', 'http://finance.ce.cn/stock/', 'http://tech.ce.cn/',
                'http://tech.ce.cn/news/', 'http://tech.ce.cn/tech2018/kjmq/', 'http://tech.ce.cn/tech2018/kx/',
                'http://tech.ce.cn/tech2018/rgzn/', 'http://tech.ce.cn/tech2018/life/', 'http://tech.ce.cn/tech2018/newtech/',
                'http://tech.ce.cn/tech2018/safe/', 'http://tech.ce.cn/tech2018/zxjy/', 'http://finance.ce.cn/stock/gsgdbd/index.shtml',
                'http://finance.ce.cn/', 'http://finance.ce.cn/shqgc/index.shtml', 'http://finance.ce.cn/zjjp/index.shtml',
                'http://finance.ce.cn/home/zqzq/dp/', 'http://finance.ce.cn/home/jrzq/dc/index.shtml', 'http://finance.ce.cn/10cjsy/bg/',
                'http://finance.ce.cn/10cjsy/hw/', 'http://finance.ce.cn/10cjsy/qt/', 'http://finance.ce.cn/home/cfzq/zq/',
                'http://finance.ce.cn/sub/ggttk/index.shtml', 'http://finance.ce.cn/sub/cj2009/index.shtml', 'http://finance.ce.cn/10cjsy/bk/',
                'http://finance.ce.cn/jjpd/index.shtml', 'http://finance.ce.cn/futures/', 'http://finance.ce.cn/gold/']
    }

    SETTINGS_YICAI = 'yicai'
    YICAI = {
        'NAME': SETTINGS_YICAI,
        'MONGO': SETTINGS_YICAI,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_YICAI),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_YICAI),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_YICAI),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_YICAI),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_YICAI),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_YICAI),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_YICAI, SETTINGS_YICAI),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_YICAI, SETTINGS_YICAI),
        'MAX_POOL_SIZE': 2,
        'URLS':['https://www.yicai.com/']
    }

    SETTINGS_IFENG = 'ifeng'
    IFENG = {
        'NAME': SETTINGS_IFENG,
        'MONGO': SETTINGS_IFENG,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_IFENG),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_IFENG),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_IFENG),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_IFENG),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_IFENG),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_IFENG),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_IFENG, SETTINGS_IFENG),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_IFENG, SETTINGS_IFENG),
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://www.ifeng.com/', 'https://mil.ifeng.com/', 'http://news.ifeng.com/',
                 'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml', 'http://news.ifeng.com/mainland/',
                 'http://news.ifeng.com/world/', 'http://news.ifeng.com/taiwan/', 'http://news.ifeng.com/society/',
                 'https://pl.ifeng.com/', 'https://history.ifeng.com/', 'http://culture.ifeng.com/', 'http://culture.ifeng.com/shanklist/17-35104-',
                 'http://culture.ifeng.com/shanklist/17-35106-', 'http://culture.ifeng.com/shanklist//17-35107-',
                 'http://culture.ifeng.com/shanklist//17-35108-', 'https://pit.ifeng.com/', 'https://pit.ifeng.com/shanklist/pit/23-35162-/1/',
                 'https://pl.ifeng.com/shanklist/original/21-35136-', 'http://news.ifeng.com/listpage/70374/1/list.shtml',
                 'http://news.ifeng.com/mainland/xuanzhan2020/', 'http://news.ifeng.com/o/dynpage/56-/1/plist.shtml',
                 'http://news.ifeng.com/listpage/111175/1/list.shtml', 'http://finance.ifeng.com/', 'http://finance.ifeng.com/shanklist/1-66-',
                 'http://finance.ifeng.com/stock/', 'http://finance.ifeng.com/hk', 'http://finance.ifeng.com/gold/',
                 'http://tech.ifeng.com/', 'http://tech.ifeng.com/digi/', 'http://tech.ifeng.com/mobile/', 'http://tech.ifeng.com/24h/',
                 'http://tech.ifeng.com/core/', 'http://tech.ifeng.com/lab/', 'http://tech.ifeng.com/profound/', 'http://tech.ifeng.com/blockchain/',
                 'http://tech.ifeng.com/autotech', 'https://tech.ifeng.com/shanklist/5-75005-75006-', 'http://tech.ifeng.com/shanklist/5-75005-75007-',
                 'http://tech.ifeng.com/shanklist/5-75005-75008-', 'http://tech.ifeng.com/shanklist/5-75005-75009-', 'http://tech.ifeng.com/shanklist/5-75005-75010-',
                 'http://tech.ifeng.com/shanklist/5-75005-75011-', 'http://tech.ifeng.com/shanklist/5-75005-75012-', 'http://tech.ifeng.com/shanklist/5-75005-75013-',
                 'http://tech.ifeng.com/shanklist/5-75005-75014-', 'http://ent.ifeng.com/', 'http://ent.ifeng.com/star/', 'http://ent.ifeng.com/movie/',
                 'http://ent.ifeng.com/tv/', 'http://ent.ifeng.com/listpage/30741/1/list.shtml', 'http://ent.ifeng.com/music/',
                 'http://sports.ifeng.com/', 'http://sports.ifeng.com/gjzq/', 'http://sports.ifeng.com/zgzq/', 'http://sports.ifeng.com/nba/',
                 'http://sports.ifeng.com/zglq/', 'http://sports.ifeng.com/zhty/', 'http://sports.ifeng.com/pb/', 'https://f1.ifeng.com/listpage/101220/1/list.shtml',
                 'http://sports.ifeng.com/zgzq/', 'http://d.sports.ifeng.com/pc/special/58998/index.shtml', 'http://sports.ifeng.com/djpl/',
                 'http://d.sports.ifeng.com/pc/special/100791/index.shtml', 'http://sports.ifeng.com/lqd/', 'http://sports.ifeng.com/ydh/', 'http://sports.ifeng.com/ylt/',
                 'http://sports.ifeng.com/scsd/', 'http://house.ifeng.com/', 'http://house.ifeng.com/news', 'http://house.ifeng.com/news/policy/', 'http://house.ifeng.com/news/market/',
                 'http://house.ifeng.com/news/sec/', 'http://house.ifeng.com/industry/companies/', 'http://house.ifeng.com/news/buying/', 'http://house.ifeng.com/house/daogou/',
                 'http://house.ifeng.com/news/dujia/', 'http://house.ifeng.com/news/view/', 'http://house.ifeng.com/industry/land/', 'http://history.ifeng.com/',
                 'http://history.ifeng.com/shanklist/15-35075-', 'http://history.ifeng.com/shanklist/original/15-35076-']
    }

    SETTINGS_JINGJI21 = 'jingji21'
    JINGJI21 = {
        'NAME': SETTINGS_JINGJI21,
        'MONGO': SETTINGS_JINGJI21,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_JINGJI21),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_JINGJI21, SETTINGS_JINGJI21),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_JINGJI21, SETTINGS_JINGJI21),
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://www.21jingji.com/', 'http://www.21jingji.com/channel/politics/']
    }

    SETTINGS_STCN = 'stcn'
    STCN = {
        'NAME': SETTINGS_STCN,
        'MONGO': SETTINGS_STCN,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_STCN),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_STCN),
        'WORK_PATH_PRD2': "{0}//{1}".format(RSYNC_PRD2, SETTINGS_STCN),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_STCN),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_STCN),
        'FINISHED_URL_PATH': "{0}//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_STCN),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_STCN, SETTINGS_STCN),
        'URL_PATH': "{0}//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_STCN, SETTINGS_STCN),
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://www.stcn.com/', 'http://news.stcn.com/', 'http://kuaixun.stcn.com/index.shtml',
                 'http://news.stcn.com/roll/', 'http://news.stcn.com/sdbd/', 'http://news.stcn.com/xwpl/',
                 'http://news.stcn.com/sbgc/', 'http://space.stcn.com/', 'http://stock.stcn.com/',
                 'http://stock.stcn.com/dapan/index.shtml', 'http://stock.stcn.com/bankuai/index.shtml',
                 'http://stock.stcn.com/xingu/index.shtml', 'http://stock.stcn.com/zhuli/index.shtml',
                 'http://kuaixun.stcn.com/list/kxyb.shtml', 'http://company.stcn.com/', 'http://zt.stcn.com/',
                 'http://news.stcn.com/gzlfzzl/', 'http://finance.stcn.com/', 'http://news.stcn.com/xwct/',
                 'http://company.stcn.com/gsdt/', 'http://yq.stcn.com/', 'http://data.stcn.com/',
                 'http://data.stcn.com/list/djsj.shtml', 'http://data.stcn.com/list/djsj.shtml', 'http://data.stcn.com/zijinliuxiang/']
    }