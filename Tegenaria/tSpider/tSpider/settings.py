# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from middlewares.fileIOMiddleware import FileIOMiddleware
from datetime import timedelta
from datetime import datetime
import time
class Settings():

    def __init__(self):
        self.file = FileIOMiddleware()
        self.RSYNC_PRD1 = "/home/dev/Data/rsyncData/prd4"
        self.RSYNC_PRD2 = "/home/dev/Data/rsyncData/prd3"
        self.CAMEL_FOOD = "/home/dev/Repository/news/Tegenaria/tSpider/tSpider/food"
        self.SITES_INFO = "/home/dev/Repository/news/Tegenaria/tSpider/tSpider/cobwebs/sites_info.txt"
        self.SITES_DEBUG = "/home/dev/Repository/news/Tegenaria/tSpider/tSpider/cobwebs/sites_debug.txt"

        self.SELENIUM_TIMEOUT = 120 #second
        self.CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

        #concurrency
        self.REFRESH_CONCURRENCY_INTERVAL = 30  #minute
        self.MAX_CONCURRENCY = 10
        self.CONCURRENCY_FILE = "{0}/max_concurrency.txt".format(self.RSYNC_PRD2)
        self.CONCURRENCY_REFRESH_FILE = "{0}/concurrency_refresh.txt".format(self.RSYNC_PRD2)

        self.REFRESH_CONCURRENCY_INTERVAL_SPIDER = 30  # minute
        self.MAX_CONCURRENCY_SPIDER = 10
        self.CONCURRENCY_FILE_SPIDER = "{0}/max_concurrency.txt".format(self.RSYNC_PRD1)
        self.CONCURRENCY_REFRESH_FILE_SPIDER = "{0}/concurrency_refresh.txt".format(self.RSYNC_PRD1)

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

        self.LOG_PATH = "{0}/log".format(self.RSYNC_PRD1)
        self.LOG_PATH_PRD2 = "{0}/log".format(self.RSYNC_PRD2)

        self.MONGO_URI = 'mongodb://127.0.0.1:27017'
        self.MONGO_DEEPINEWS = 'DeepNewsDatabase'

        self.REDIS_HOST = '127.0.0.1'
        self.REDIS_PORT = 6379

        self.BLOOMFILTER_URLS = "tegenaria:urls"
        self.BLOOMFILTER_CONTENT = "tegenaria:content"
        self.BLOOMFILTER_AUTHORS = "tegenaria:authors"

        self.TODAY = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        self.CHRONUS_SETTINGS = "{0}/log/chronus.csv".format(self.RSYNC_PRD1)

        self.DISABLE_RESTART_INTERVAL = False

        #sogo-sogo-weixin
        self.VALID_PROXY_POOL_SOGO_ACCOUNT = "valid_proxy_pool:sogo_account"
        self.INVALID_PROXY_POOL_SOGO_ACCOUNT = "invalid_proxy_pool:sogo_account"
        self.VALID_PROXY_POOL_SOGO_ARTICLE_LIST = "valid_proxy_pool:sogo_article_list"
        self.INVALID_PROXY_POOL_SOGO_ARTICLE_LIST = "invalid_proxy_pool:sogo_article_list"
        self.VALID_PROXY_POOL_WX = "valid_proxy_pool:wx"
        self.INVALID_PROXY_POOL_WX = "invalid_proxy_pool:wx"
        self.FINISHED_SOGO_ACCOUNT = "finished:sogo_account"
        self.FINISHED_SOGO_ARTICLE_LIST = "finished:sogo_article_list"
        self.FINISHED__WX = "finished:wx"

        # shenjian-weixin
        self.FINISHED_WEIXIN_URL_ID = "finished:weixin_url_id"
        self.FINISHED_WEIXIN_URL_ARTICLE = "finished:weixin_url_article"
        self.FINISHED_WEIXIN_CONTENT_ARTICLE = "finished:weixin_content_article"

        #sites
        self.URL_DEEPINEWS_10002_ARTICLE = "http://www.deepinews.com:10002/article/"
        self.URL_DEEPINEWS_10002_IMAGE = 'http://www.deepinews.com:10002/img/'
        # self.URL_DEEPINEWS_10002_ARTICLE = 'http://192.168.163.26:8081/article/'
        # self.URL_DEEPINEWS_10002_IMAGE = 'http://192.168.163.26:8081/img/'

        #images filter
        self.FINISHED_IMAGE_ID = "finished:image_id"

        #temp folder for html and img
        self.TEMP_FOLDER_HTML = "/home/dev/Data/Production/data4deepinews/html"
        self.TEMP_FOLDER_IMG = "/home/dev/Data/Production/data4deepinews/img"
        self.FINISHED_TEMP_WEIXIN = "finished:temp_weixin"

        #remove server information
        self.HOST_NAME = '223.111.139.227'
        self.USER_NAME = 'root'
        self.PASSWORD = 'rerr48779'
        self.PORT = 22
        self.REMOTE_IMG_PATH = '/home/dev/Data/Production/img_tmp'
        self.REMOTE_HTML_PATH = '/home/dev/Data/Production/html_tmp'
        self.MAX_UPLOAD_PROCESS = 20

        #refresh the redis interval
        self.REFRESH_REDIS_INTERVAL = 1440

        #huxiu_nlp
        self.FINISHED_HUXIU_NLP = "finished:huxiu_nlp"

        #mongodb
        self.SPIDERDB = "SPIDERS"

        #article url
        self.ARTICLE_URL = "https://www.deepinews.com/article/"

        #aliyun
        self.ALI_DOMAIN = "oss-cn-beijing.aliyuncs.com"
        self.ALI_BUCKET_NAME_DEEPINEWS = "deepinews"
        self.ALI_BUCKET_NAME_DEEPINEWS_IMG = "img"

        # local html info
        self.LOCAL_HTML_PATH = "{0}/local".format(self.RSYNC_PRD1)

        # webserver0 html info
        self.IP_WEBSERVER0 = "223.111.139.227"
        self.PORT_WEBSERVER0 = 22
        self.USER_ROOT_WEBSERVER0 = "root"
        self.USER_ROOT_PASSWORD_WEBSERVER0 = "rerr48779"
        self.HTML_WEBSERVER0 = "/home/dev/Data/Production/article"
        self.RETRY_FILE = "{0}/retry.txt".format(self.RSYNC_PRD1)
        self.UPLOAD_HTML_API = "https://www.deepinews.com/api/articles/uploadhtml"

        #webserver0 mongo data info
        self.LOCAL_MONGO_DATA_PATH = "/home/dev/Data/Production/data4deepinews/{0}.csv".format(self.TODAY)
        self.REMOTE_MONGO_DATA_PATH = "/home/dev/Data/Production/data4deepinews/{0}.csv".format(self.TODAY)

        #template
        self.TEMPLATE_PATH = "/home/dev/Repository/news/Tegenaria/tSpider/tSpider/storeHtml/template_1.html"

        #monitor
        self.MONITOR_SPIDERS_URL = "https://www.deepinews.com/sites/index.html"
        self.MONITOR_SITE_URL = "https://www.deepinews.com/sites/"
        self.MONITOR_SPIDERS_TEMPLATE_PATH = \
            "/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiderMonitor/index.html"
        self.MONITOR_SITE_TEMPLATE_PATH = \
            "/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiderMonitor/site.html"
        self.MONITOR_UPLOAD_LOCAL = "{0}/monitor".format(self.RSYNC_PRD1)
        self.MONITOR_UPLOAD_PATH_WEBSERVER0 = "/home/dev/Data/Production"
        self.MONITOR_SITE_HTML_WEBSERVER0 = "/home/dev/Data/Production/statics/sites"

    def SettingsFormat(self,
                       SETTINGS_NAME,
                       SOURCE_NAME,
                       RESTART_INTERVAL,
                       MAX_POOL_SIZE_URL,
                       MAX_POOL_SIZE_CONTENT,
                       IS_OPEN_CACHE,
                       START_TIME,
                       END_TIME,
                       URL_TIMEOUT,
                       CONTENT_TIMEOUT):
        return settingsSpec(SETTINGS_NAME,
                            SOURCE_NAME,
                            RESTART_INTERVAL,
                            MAX_POOL_SIZE_URL,
                            MAX_POOL_SIZE_CONTENT,
                            IS_OPEN_CACHE,
                            START_TIME,
                            END_TIME,
                            URL_TIMEOUT,
                            CONTENT_TIMEOUT)

    def CreateSettings(self, siteinfo=None):
        print "Create setting for: {0}".format(siteinfo.domain)
        return self.SettingsFormat(siteinfo.domain,
                                   siteinfo.name,
                                   siteinfo.restart_interval,
                                   siteinfo.url_parallel_number,
                                   siteinfo.content_parallel_number,
                                   siteinfo.is_open_cache,
                                   siteinfo.work_time_start,
                                   siteinfo.work_time_end,
                                   siteinfo.url_timeout,
                                   siteinfo.content_timeout)

    def CreateCommonSettings(self):
        return self.SettingsFormat('0', '0', '0', '0', '0', '0', '0', '0', '0', '0')

class settingsSpec():
    def __init__(self,
                 SETTINGS_NAME=None,
                 SOURCE_NAME=None,
                 RESTART_INTERVAL=None,
                 MAX_POOL_SIZE_URL=None,
                 MAX_POOL_SIZE_CONTENT=None,
                 IS_OPEN_CACHE=None,
                 START_TIME=None,
                 END_TIME=None,
                 URL_TIMEOUT=None,
                 CONTENT_TIMEOUT=None):
        settings = Settings()
        self.NAME = SETTINGS_NAME
        self.MONGO = SETTINGS_NAME
        self.MONGO_URLS = "{0}_urls".format(SETTINGS_NAME)
        self.WORK_PATH_PRD1 = "{0}/sites/{1}".format(settings.RSYNC_PRD1,
                                                       SETTINGS_NAME)
        self.WORK_PATH_PRD2 = "{0}/sites/{1}".format(settings.RSYNC_PRD2,
                                                       SETTINGS_NAME)
        self.FINISHED_TXT_PATH = "{0}/sites/{1}/txt/{2}".format(settings.RSYNC_PRD1,
                                                                    SETTINGS_NAME,
                                                                    settings.TODAY)
        self.FINISHED_HTML_PATH = "{0}/sites/{1}/html/{2}".format(settings.RSYNC_PRD1,
                                                                      SETTINGS_NAME,
                                                                      settings.TODAY)
        self.FINISHED_IMG_PATH = "{0}/sites/{1}/img/{2}".format(settings.RSYNC_PRD1,
                                                                    SETTINGS_NAME,
                                                                    settings.TODAY)
        self.FINISHED_CONTENT_PATH = "{0}/sites/{1}/{2}_content.csv".format(settings.RSYNC_PRD1,
                                                                               SETTINGS_NAME,
                                                                               SETTINGS_NAME)
        self.FINISHED_BACKUP_FOLDER_PATH = "{0}/sites/{1}/mongo/{2}".format(settings.RSYNC_PRD1,
                                                                                SETTINGS_NAME,
                                                                                settings.TODAY)
        self.FINISHED_BACKUP_PATH = "{0}/sites/{1}/mongo/{2}/{3}_content_bk.csv".format(settings.RSYNC_PRD1,
                                                                                             SETTINGS_NAME,
                                                                                             settings.TODAY,
                                                                                             SETTINGS_NAME)
        self.FINISHED_BACKUP_POST_PATH = "{0}/sites/{1}/mongo/{2}/{3}_content_bk.csv".format(settings.RSYNC_PRD1,
                                                                                                  SETTINGS_NAME,
                                                                                                  settings.YESTERDAY,
                                                                                                  SETTINGS_NAME)
        self.URL_PATH = "{0}/sites/{1}/{2}_urls.csv".format(settings.RSYNC_PRD2,
                                                               SETTINGS_NAME,
                                                               SETTINGS_NAME)
        self.URL_BACKUP_FOLDER_PATH = "{0}/sites/{1}/mongo/{2}".format(settings.RSYNC_PRD2,
                                                                           SETTINGS_NAME,
                                                                           settings.TODAY)
        self.URL_BACKUP_PATH = "{0}/sites/{1}/mongo/{2}/{3}_urls_bk.csv".format(settings.RSYNC_PRD2,
                                                                                     SETTINGS_NAME,
                                                                                     settings.TODAY,
                                                                                     SETTINGS_NAME)
        self.URL_BACKUP_POST_PATH = "{0}/sites/{1}/mongo/{2}/{3}_urls_bk.csv".format(settings.RSYNC_PRD2,
                                                                                          SETTINGS_NAME,
                                                                                          settings.YESTERDAY,
                                                                                          SETTINGS_NAME)
        self.AUTHORS_PATH = "{0}/sites/{1}".format(settings.RSYNC_PRD2,
                                                     SETTINGS_NAME)
        self.RESTART_PATH = "{0}/sites/{1}/restart.txt".format(settings.RSYNC_PRD2,
                                                                  SETTINGS_NAME)
        self.REDIS_REFRESH_PATH = "{0}/sites/{1}/redis_refresh.txt".format(settings.RSYNC_PRD2,
                                                                              SETTINGS_NAME)
        self.RESTART_INTERVAL = int(RESTART_INTERVAL)
        self.MAX_POOL_SIZE_URL = int(MAX_POOL_SIZE_URL)
        self.MAX_POOL_SIZE_CONTENT = int(MAX_POOL_SIZE_CONTENT)
        self.URLS = "{0}/{1}.txt".format(settings.CAMEL_FOOD, SETTINGS_NAME)
        self.IS_OPEN_CACHE = str(IS_OPEN_CACHE) == "True"
        self.SOURCE_NAME = SOURCE_NAME
        self.START_TIME = START_TIME
        self.END_TIME = END_TIME
        self.URL_TIMEOUT = int(URL_TIMEOUT)
        self.CONTENT_TIMEOUT = int(CONTENT_TIMEOUT)