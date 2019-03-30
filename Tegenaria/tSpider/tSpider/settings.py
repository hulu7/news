# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.fileIOMiddleware import FileIOMiddleware
import time
class Settings():

    def __init__(self):
        self.file = FileIOMiddleware()
        self.RSYNC_PRD1 = "//home//dev//Data//rsyncData//prd4"
        self.RSYNC_PRD2 = "//home//dev//Data//rsyncData//prd3"
        self.CAMEL_FOOD = "//home//dev//Repository//news//Tegenaria//tSpider//tSpider//food"
        self.COBWEBS = "//home//dev//Repository//news//Tegenaria//tSpider//tSpider//cobwebs/silk.txt"

        self.SELENIUM_TIMEOUT = 300
        self.CHROMEDRIVER_PATH = "//usr//bin//chromedriver"

        self.USER_AGENTS = [
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
        self.ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        self.ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9,en;q=0.8"
        self.ACCEPT_ENC0DING = "gzip, deflate"
        self.CONNECTION = "keep-alive"
        self.CACHE_CONTROL = "max-age=0"
        self.PRAGMA = "no-cache"
        self.UPGRADE_INSECURE_REQUESTS = "1"

        self.LOG_PATH = "{0}//log".format(self.RSYNC_PRD1)
        self.LOG_PATH_PRD2 = "{0}//log".format(self.RSYNC_PRD2)

        self.MONGO_URI = 'mongodb://127.0.0.1:27017'

        self.REDIS_HOST = '127.0.0.1'
        self.REDIS_PORT = 6379

        self.BLOOMFILTER_NAME = "tegenaria:dupefilter"

        self.TODAY = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        self.CHRONUS_SETTINGS = "{0}//log//chronus.csv".format(self.RSYNC_PRD1)

        self.DISABLE_RESTART_INTERVAL = False

    def SettingsFormat(self, SETTINGS_NAME, SOURCE_NAME, RESTART_INTERVAL, MAX_POOL_SIZE, IS_OPEN_CACHE):
        return {
            'NAME': SETTINGS_NAME,
            'MONGO': SETTINGS_NAME,
            'MONGO_URLS': "{0}_urls".format(SETTINGS_NAME),
            'WORK_PATH_PRD1': "{0}//{1}".format(self.RSYNC_PRD1, SETTINGS_NAME),
            'WORK_PATH_PRD2': "{0}//sites//{1}".format(self.RSYNC_PRD2, SETTINGS_NAME),
            'FINISHED_TXT_PATH': "{0}//{1}//txt".format(self.RSYNC_PRD1, SETTINGS_NAME),
            'FINISHED_CONTENT_PATH': "{0}//{1}//{2}_content.csv".format(self.RSYNC_PRD1, SETTINGS_NAME, SETTINGS_NAME),
            'URL_PATH': "{0}//sites//{1}//{2}_urls.csv".format(self.RSYNC_PRD2, SETTINGS_NAME, SETTINGS_NAME),
            'RESTART_PATH': "{0}//sites//{1}//restart.txt".format(self.RSYNC_PRD2, SETTINGS_NAME),
            'RESTART_INTERVAL': int(RESTART_INTERVAL),
            'MAX_POOL_SIZE': int(MAX_POOL_SIZE),
            'URLS': "{0}//{1}.txt".format(self.CAMEL_FOOD, SETTINGS_NAME),
            'IS_OPEN_CACHE': str(IS_OPEN_CACHE) == "True",
            'SOURCE_NAME': SOURCE_NAME
        }

    def CreateSettings(self, NAME):
        content = self.file.readFromTxt(self.COBWEBS)
        config_list = content.split('\n')
        for config in config_list:
            if NAME in config:
                print "Find the :{0}".format(NAME)
                data = config.split(',')
                return self.SettingsFormat(data[0], data[1], data[2], data[3], data[4])
        print "Cannot find the :{0}".format(NAME)

    def CreateCommonSettings(self):
        return self.SettingsFormat('0', '0', '0', '0','0')