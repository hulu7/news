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

    MONGO_URI = 'mongodb://127.0.0.1:27017'

    CHRONUS_SETTINGS = "{0}//log//chronus.csv".format(RSYNC_PRD1)

    SETTINGS_HUXIU = 'huxiu'
    HUXIU = {
        'NAME': SETTINGS_HUXIU,
        'MONGO': SETTINGS_HUXIU,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_HUXIU),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_HUXIU),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_HUXIU, SETTINGS_HUXIU),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_HUXIU, SETTINGS_HUXIU),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_HUXIU),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://www.huxiu.com/']
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
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_CE),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_CE, SETTINGS_CE),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_CE, SETTINGS_CE),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_CE),
        'RESTART_INTERVAL': 20,
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://m.ce.cn', 'http://m.ce.cn/yw/', 'http://m.ce.cn/cj/', 'http://m.ce.cn/gp/',
                'http://m.ce.cn/gj/', 'http://m.ce.cn/gs/', 'http://m.ce.cn/lc/', 'http://m.ce.cn/lv/fo/',
                'http://m.ce.cn/qc/', 'http://m.ce.cn/fc/', 'http://m.ce.cn/fa/', 'http://m.ce.cn/lv/',
                'http://m.ce.cn/sh/', 'http://m.ce.cn/lv/jk/']
    }

    SETTINGS_EEO = 'eeo'
    EEO = {
        'NAME': SETTINGS_EEO,
        'MONGO': SETTINGS_EEO,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_EEO),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_EEO),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_EEO),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_EEO),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_EEO),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_EEO),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_EEO, SETTINGS_EEO),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_EEO, SETTINGS_EEO),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_EEO),
        'RESTART_INTERVAL': 120,
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://m.eeo.com.cn/', 'http://m.eeo.com.cn/yaowen/sxgd/', 'http://m.eeo.com.cn/yaowen/dzsp/',
                 'http://m.eeo.com.cn/jinrong/xinsanban/', 'http://m.eeo.com.cn/jinrong/hlwjr/',
                 'http://m.eeo.com.cn/shangye/hualeizhiyue/', 'http://m.eeo.com.cn/shangye/cyjbj/',
                 'http://m.eeo.com.cn/yaowen/dashi/', 'http://m.eeo.com.cn/yaowen/hfggzc/',
                 'http://m.eeo.com.cn/yaowen/hfshuju/', 'http://m.eeo.com.cn/yaowen/hfdongjian/',
                 'http://m.eeo.com.cn/jinrong/zhengquan/', 'http://m.eeo.com.cn/jinrong/zhaishi/',
                 'http://m.eeo.com.cn/jinrong/ziben/', 'http://m.eeo.com.cn/jinrong/licai/',
                 'http://m.eeo.com.cn/shangye/xinnengyuan/', 'http://m.eeo.com.cn/shangye/yiliao/',
                 'http://m.eeo.com.cn/shangye/wuliu/', 'http://m.eeo.com.cn/shangye/dianshang/',
                 'http://m.eeo.com.cn/fcqcxf/dichan/', 'http://m.eeo.com.cn/yule/yingshi/',
                 'http://m.eeo.com.cn/fcqcxf/qiche/', 'http://m.eeo.com.cn/fcqcxf/xiaofei/',
                 'http://m.eeo.com.cn/yule/yule/', 'http://m.eeo.com.cn/yule/tiyu/',
                 'http://m.eeo.com.cn/gcj/guanchajia/', 'http://m.eeo.com.cn/gcj/shuping/',
                 'http://m.eeo.com.cn/gcj/zhuanlan/', 'http://m.eeo.com.cn/gcj/lingdu/'
                 'http://m.eeo.com.cn/zixun/']
    }

    SETTINGS_HUANQIU = 'huanqiu'
    HUANQIU = {
        'NAME': SETTINGS_HUANQIU,
        'MONGO': SETTINGS_HUANQIU,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_HUANQIU),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_HUANQIU),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_HUANQIU),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_HUANQIU),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_HUANQIU),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_HUANQIU),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_HUANQIU, SETTINGS_HUANQIU),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_HUANQIU, SETTINGS_HUANQIU),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_HUANQIU),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://m.huanqiu.com/', 'https://m.huanqiu.com/#channel=world', 'https://m.huanqiu.com/#channel=taihai',
                 'https://m.huanqiu.com/#channel=society', 'https://m.huanqiu.com/#channel=mil', 'https://m.huanqiu.com/#channel=editorial',
                 'https://m.huanqiu.com/#channel=inland', 'https://m.huanqiu.com/#channel=comment', 'https://m.huanqiu.com/#channel=oversea',
                 'https://m.huanqiu.com/#channel=finance', 'https://m.huanqiu.com/#channel=chamber', 'https://m.huanqiu.com/#channel=auto',
                 'https://m.huanqiu.com/#channel=tech', 'https://m.huanqiu.com/#channel=smart', 'https://m.huanqiu.com/#channel=shanrenping',
                 'https://m.huanqiu.com/#channel=uav', 'https://m.huanqiu.com/#channel=travel', 'https://m.huanqiu.com/#channel=health',
                 'https://m.huanqiu.com/#channel=ent', 'https://m.huanqiu.com/#channel=art', 'https://m.huanqiu.com/#channel=fashion',
                 'https://m.huanqiu.com/#channel=women', 'https://m.huanqiu.com/#channel=sports', 'https://m.huanqiu.com/#channel=bigdata',
                 'https://m.huanqiu.com/#channel=ski', 'https://m.huanqiu.com/#channel=liuxue', 'https://m.huanqiu.com/#channel=city',
                 'https://m.huanqiu.com/#channel=business']
    }

    SETTINGS_CANKAOXIAOXI = 'cankaoxiaoxi'
    CANKAOXIAOXI = {
        'NAME': SETTINGS_CANKAOXIAOXI,
        'MONGO': SETTINGS_CANKAOXIAOXI,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_CANKAOXIAOXI),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_CANKAOXIAOXI, SETTINGS_CANKAOXIAOXI),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI, SETTINGS_CANKAOXIAOXI),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_CANKAOXIAOXI),
        'RESTART_INTERVAL': 10,
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://m.cankaoxiaoxi.com/', 'http://m.cankaoxiaoxi.com/home/', 'http://m.cankaoxiaoxi.com/mil/',
                 'http://m.cankaoxiaoxi.com/finance/', 'http://m.cankaoxiaoxi.com/world/', 'http://m.cankaoxiaoxi.com/column/',
                 'http://m.cankaoxiaoxi.com/culture/', 'http://m.cankaoxiaoxi.com/science/', 'http://m.cankaoxiaoxi.com/special/',
                 'http://m.cankaoxiaoxi.com/ym/', 'http://m.cankaoxiaoxi.com/chuhaiji/']
    }

    SETTINGS_GUANCHA = 'guancha'
    GUANCHA = {
        'NAME': SETTINGS_GUANCHA,
        'MONGO': SETTINGS_GUANCHA,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_GUANCHA),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_GUANCHA),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_GUANCHA),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_GUANCHA),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_GUANCHA),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_GUANCHA),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_GUANCHA, SETTINGS_GUANCHA),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_GUANCHA, SETTINGS_GUANCHA),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_GUANCHA),
        'RESTART_INTERVAL': 5,
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://m.guancha.cn/', 'https://m.guancha.cn/politics', 'https://m.guancha.cn/#shiping',
                 'https://m.guancha.cn/#gundong']
    }

    SETTINGS_YICAI = 'yicai'
    YICAI = {
        'NAME': SETTINGS_YICAI,
        'MONGO': SETTINGS_YICAI,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_YICAI),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_YICAI),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_YICAI),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_YICAI),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_YICAI),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_YICAI),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_YICAI, SETTINGS_YICAI),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_YICAI, SETTINGS_YICAI),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_YICAI),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS':['https://m.yicai.com/', 'https://m.yicai.com/news/gushi/', 'https://m.yicai.com/news/hongguan/',
                'https://m.yicai.com/news/minsheng/', 'https://m.yicai.com/news/policy/', 'https://m.yicai.com/news/gaige/',
                'https://m.yicai.com/news/jinrong/', 'https://m.yicai.com/news/quanqiushichang/', 'https://m.yicai.com/news/gongsi/',
                'https://m.yicai.com/news/jiankangshenghuo/', 'https://m.yicai.com/news/shijie/', 'https://m.yicai.com/news/kechuang/',
                'https://m.yicai.com/news/quyu/', 'https://m.yicai.com/news/comment/', 'https://m.yicai.com/news/dafengwenhua/',
                'https://m.yicai.com/news/books/', 'https://m.yicai.com/news/loushi/', 'https://m.yicai.com/news/automobile/',
                'https://m.yicai.com/news/fashion/', 'https://m.yicai.com/news/ad/']
    }

    SETTINGS_IFENG = 'ifeng'
    IFENG = {
        'NAME': SETTINGS_IFENG,
        'MONGO': SETTINGS_IFENG,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_IFENG),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_IFENG),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_IFENG),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_IFENG),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_IFENG),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_IFENG),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_IFENG, SETTINGS_IFENG),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_IFENG, SETTINGS_IFENG),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_IFENG),
        'RESTART_INTERVAL': 5,
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://i.ifeng.com/', 'http://ient.ifeng.com/', 'https://i.ifeng.com/idyn/ient/0/3/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/ient/0/6/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/ient/0/1370/0/10/10/list.shtml',
                 'http://ifinance.ifeng.com/', 'http://ifinance.ifeng.com/marketsf.shtml',
                 'https://istock.ifeng.com/', 'https://i.ifeng.com/idyn/ifinance/0/597/listsf.shtml',
                 'https://i.ifeng.com/idyn/ifinance/0/111/listsf.shtml', 'https://imil.ifeng.com',
                 'https://i.ifeng.com/idyn/inews/0/4550/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/inews/0/7128/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/inews/0/7106/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/inews/0/7129/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/inews/0/7131/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/inews/0/7130/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/inews/0/7104/0/10/10/list.shtml', 'http://itech.ifeng.com/', 'http://tech.ifeng.com/mobile/',
                 'http://tech.ifeng.com/digi/', 'http://tech.ifeng.com/24h/', 'http://tech.ifeng.com/core/', 'http://tech.ifeng.com/lab/',
                 'http://tech.ifeng.com/profound/', 'http://tech.ifeng.com/blockchain/', 'http://tech.ifeng.com/autotech',
                 'https://isports.ifeng.com/', 'https://isports.ifeng.com/ispecial/29/index.shtml', 'https://isports.ifeng.com/run/index.shtml',
                 'https://isports.ifeng.com/ispecial/28/index.shtml', 'https://i.ifeng.com/idyn/inews/0/54063/0/10/10/list.shtml',
                 'https://isports.ifeng.com/ispecial/81/index.shtml', 'https://isports.ifeng.com/ispecial/80/index.shtml',
                 'https://i.ifeng.com/idyn/inews/0/11247/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/inews/0/11243/0/10/10/list.shtml',
                 'https://iauto.ifeng.com', 'http://ihouse.ifeng.com/', 'https://iauto.ifeng.com', 'https://iauto.ifeng.com/?c=index&a=cat&id=564',
                 'https://iauto.ifeng.com/?c=index&a=cat&id=587', 'https://iauto.ifeng.com/quanmeiti/#/', 'http://ifenghuanghao.ifeng.com/',
                 'http://ifashion.ifeng.com', 'https://i.ifeng.com/idyn/ifashion/0/2880/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/ifashion/0/2884/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/ifashion/0/2908/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/ifashion/0/2903/0/10/10/list.shtml', 'https://ihistory.ifeng.com', 'https://i.ifeng.com/idyn/inews/0/4762/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/inews/0/4763/0/10/10/list.shtml', 'https://i.ifeng.com/idyn/inews/0/4764/0/10/10/list.shtml',
                 'https://i.ifeng.com/idyn/inews/0/4766/0/10/10/list.shtml', 'https://itaiwan.ifeng.com/index.shtml', 'https://igangao.ifeng.com/index.shtml',
                 'https://ipl.ifeng.com/', 'https://itravel.ifeng.com/', 'https://ihealth.ifeng.com/', 'https://iculture.ifeng.com/',
                 'https://iguoxue.ifeng.com', 'https://ipit.ifeng.com/', 'https://i.ifeng.com/idyn/inews/0/7720/0/10/10/list.shtml',
                 'https://isports.ifeng.com/ispecial/29/index.shtml', 'https://if1.ifeng.com/']
    }

    SETTINGS_JINGJI21 = 'jingji21'
    JINGJI21 = {
        'NAME': SETTINGS_JINGJI21,
        'MONGO': SETTINGS_JINGJI21,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_JINGJI21),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_JINGJI21),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_JINGJI21, SETTINGS_JINGJI21),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_JINGJI21, SETTINGS_JINGJI21),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_JINGJI21),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://m.21jingji.com/', 'https://m.21jingji.com/channel/finance', 'https://m.21jingji.com/channel/politics',
                 'https://m.21jingji.com/channel/capital', 'https://m.21jingji.com/channel/business', 'https://m.21jingji.com/channel/opinion',
                 'https://m.21jingji.com/channel/technology', 'https://m.21jingji.com/channel/life', 'https://m.21jingji.com/channel/global',
                 'https://m.21jingji.com/channel/entrepreneur', 'https://m.21jingji.com/channel/19th', 'https://m.21jingji.com/channel/21tv',
                 'https://m.21jingji.com/channel/TVS1', 'https://m.21jingji.com/channel/marathon', 'https://m.21jingji.com/channel/BandR',
                 'https://m.21jingji.com/channel/readnumber', 'https://m.21jingji.com/channel/GHM_GreaterBay', 'https://m.21jingji.com/channel/Property',
                 'https://m.21jingji.com/channel/AIWriter', 'https://m.21jingji.com/channel/ftz', 'https://m.21jingji.com/channel/investment']
    }

    SETTINGS_STCN = 'stcn'
    STCN = {
        'NAME': SETTINGS_STCN,
        'MONGO': SETTINGS_STCN,
        'MONGO_URLS': "{0}_urls".format(SETTINGS_STCN),
        'WORK_PATH_PRD1': "{0}//{1}".format(RSYNC_PRD1, SETTINGS_STCN),
        'WORK_PATH_PRD2': "{0}//sites//{1}".format(RSYNC_PRD2, SETTINGS_STCN),
        'FINISHED_TXT_PATH': "{0}//{1}//txt".format(RSYNC_PRD1, SETTINGS_STCN),
        'FINISHED_ID_PATH': "{0}//{1}//finished_id.csv".format(RSYNC_PRD1, SETTINGS_STCN),
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_STCN),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_STCN, SETTINGS_STCN),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_STCN, SETTINGS_STCN),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_STCN),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': ['http://www.stcn.com/', 'http://news.stcn.com/', 'http://kuaixun.stcn.com/index.shtml',
                 'http://news.stcn.com/roll/', 'http://news.stcn.com/sdbd/', 'http://news.stcn.com/xwpl/',
                 'http://news.stcn.com/sbgc/', 'http://space.stcn.com/', 'http://stock.stcn.com/',
                 'http://stock.stcn.com/dapan/index.shtml', 'http://stock.stcn.com/bankuai/index.shtml',
                 'http://stock.stcn.com/xingu/index.shtml', 'http://stock.stcn.com/zhuli/index.shtml',
                 'http://kuaixun.stcn.com/list/kxyb.shtml', 'http://company.stcn.com/',
                 'http://news.stcn.com/gzlfzzl/', 'http://finance.stcn.com/', 'http://news.stcn.com/xwct/',
                 'http://company.stcn.com/gsdt/', 'http://yq.stcn.com/', 'http://data.stcn.com/',
                 'http://data.stcn.com/list/djsj.shtml', 'http://data.stcn.com/list/djsj.shtml', 'http://data.stcn.com/zijinliuxiang/']
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
        'FINISHED_URL_PATH': "{0}//sites//{1}//finished_url.csv".format(RSYNC_PRD2, SETTINGS_WALLSTREETCN),
        'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(RSYNC_PRD1, SETTINGS_WALLSTREETCN, SETTINGS_WALLSTREETCN),
        'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(RSYNC_PRD2, SETTINGS_WALLSTREETCN, SETTINGS_WALLSTREETCN),
        'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(RSYNC_PRD2, SETTINGS_WALLSTREETCN),
        'RESTART_INTERVAL': 30,
        'MAX_POOL_SIZE': 2,
        'URLS': ['https://m.wallstreetcn.com/news/global',
                 'https://wallstreetcn.com/?from=navbar',
                 '']
    }