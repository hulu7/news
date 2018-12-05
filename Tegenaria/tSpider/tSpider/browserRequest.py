# -*- coding: utf-8 -*-
#------requirement------
#selenium-3.14.1
#Scrapy-1.5.1
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from multiprocessing.pool import ThreadPool as Pool
import gc
from settings import Settings
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.seleniumMiddleware import SeleniumMiddleware

class BrowserRequest():
    def run_task(self, url, callback=callable):
        self.file.logger(Settings.LOG_PATH, 'Start: %s' % url)
        print 'Start: %s' % url
        request = SeleniumMiddleware()
        request.chrome_request(url)
        response = request.browser
        try:
            callback({'response': response, 'request_url': url})
        except Exception, e:
            self.file.logger(Settings.LOG_PATH, 'Exception: %s for %' % e % url)
            print 'Exception: %s for %' % e % url
            response.close()
            response.quit()
            del response, request
            gc.collect()
        self.content.append({'current_url': response.current_url, 'page_source': response.page_source})
        self.file.logger(Settings.LOG_PATH, 'End: %s' % response.current_url)
        print 'End: %s' % response.current_url
        response.close()
        response.quit()
        del response, request
        gc.collect()

    def start_chrome(self, urls, processes, callback=callable):
        self.file = FileIOMiddleware()
        self.content = []
        process = Pool(processes)
        for url in urls:
            process.apply_async(self.run_task, args=(url,callback,))
        process.close()
        process.join()
        self.file.logger(Settings.LOG_PATH, 'Done')
        print 'Done'
        del self.file, process
        gc.collect()
        return self.content

if __name__ == '__main__':
    def show(a, b):
        print a
    browser = BrowserRequest()
    urls = ['https://www.huxiu.com/article/273272.html', 'https://www.huxiu.com/article/273269.html']
    content = browser.start_chrome(urls, 1, callback=show)
    print content