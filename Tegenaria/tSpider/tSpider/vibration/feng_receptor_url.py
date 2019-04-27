#coding:utf-8
#------requirement------
#lxml-3.2.1
#numpy-1.15.2
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time

sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from Tegenaria.tSpider.tSpider.browserRequest import BrowserRequest
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class FengReceptor():

    def __init__(self):
        self.settings = Settings()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()
        self.doraemon.createFilePath(self.work_path_prd2)

    def getSettings(self):
        self.work_path_prd2 = "//home//dev//Data//rsyncData//test//"
        self.mongo = "feng_receptor"
        self.finished_ids = "feng_receptor"
        self.log_path = "//home//dev//Data//rsyncData//test//"

    def parse(self, response):
        time.sleep(1)
        current_url = response['response'].current_url.encode('gbk')
        print 'Start to parse: {0}'.format(current_url)
        key = response['request_title'].strip()
        str = response['response'].page_source.encode('utf-8')
        str_n = str[str.find('(') + 1:-21]
        str_n = str_n.replace('null', 'None')
        dics = eval(str_n)
        if len(dics['items']) == 0:
            print 'No data for: {0}'.format(key)
            self.doraemon.hashSet(self.finished_ids, key, key)
            return
        for item in dics['items']:
            name = item['name'].replace('&lt;','').replace('em&gt;','').replace('\\/','')
            id = item['id']
            if len(id) > 0 and name == key:
                url = "https://feng.ifeng.com/author/{0}".format(id)
                self.doraemon.hashSet(self.finished_ids, key, key)
                data = {
                    'id': key,
                    'url': url
                }
                print 'Start to store mongo {0}'.format(data['url'])
                self.doraemon.storeMongodb(self.mongo, data)
                print 'Finished for {0}'.format(key)

    def start_requests(self):
        print 'Start requests'
        new_urls = []
        all_finished_id = list(self.doraemon.getAllHasSet(self.finished_ids))
        txt_path = '/home/dev/Data/rsyncData/test/feng_receptor.txt'
        gonzhonghao = self.file.readFromTxt(txt_path)
        keys = gonzhonghao.split('\n')

        for key in keys:
            key = key.strip()
            if key not in all_finished_id:
                name = key.strip()
                tmp_url = "https://so.v.ifeng.com/websearch/ifeng-search-server/sub/websearch?k={0}&page=1&distinct=1&n=10&hl=1&os=ios&gv=6.2.5&uid=70b6a1d8f6c64618bf9dfa092fc4e34c&callback=getData".format(name)
                new_urls.append([tmp_url, name])
            else:
                print 'Finished or no data for {0}'.format(key)
                self.doraemon.hashSet(self.finished_ids, key, key)

        if len(new_urls) == 0:
            print 'No more urls.'
            return

        request = BrowserRequest()
        request.start_chrome(new_urls, 5, self.log_path, None, callback=self.parse)

if __name__ == '__main__':
    fengReceptor=FengReceptor()
    fengReceptor.start_requests()