# -*- coding: utf-8 -*-
#------requirement------
#selenium-3.14.1
#Scrapy-1.5.1
#------requirement------
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
import eventlet
import gc
from multiprocessing.pool import ThreadPool as Pool
from middlewares.fileIOMiddleware import FileIOMiddleware
from middlewares.seleniumMiddleware import SeleniumMiddleware

class BrowserRequest():
    def run_task(self, url_title, url_timeout, callback=callable):
        self.file.logger(self.log_path, 'Start: {0}'.format(url_title[0]))
        print 'Start: {0}'.format(url_title[0])
        is_loading = True
        try:
            eventlet.monkey_patch()
            request = SeleniumMiddleware()
            with eventlet.Timeout(url_timeout, False):
                request.chrome_request(url_title[0], self.log_path, self.proxy)
                is_loading = False
                print 'Finish loading: {0}'.format(url_title[0])
            if is_loading:
                raise Exception('Url fetch timeout')
            response = request.browser
            callback({'response': response, 'request_url': url_title[0], 'request_title': url_title[1]})
        except Exception as e:
            self.file.logger(self.log_path, 'Exception: {0} for {1}'.format(e.message, url_title[0]))
            print 'Exception: {0} for {1}'.format(e.message, url_title[0])
            response.close()
            response.quit()
            del response, request
            gc.collect()
        self.content.append({'current_url': response.current_url, 'page_source': response.page_source})
        self.file.logger(self.log_path, 'End: {0}'.format(response.current_url))
        print 'End: {0}'.format(response.current_url)
        response.close()
        response.quit()
        del response, request
        gc.collect()

    def start_chrome(self, url_titles, url_timeout, processes, log_path, proxy, callback=callable):
        self.file = FileIOMiddleware()
        self.content = []
        self.log_path = log_path
        self.proxy = proxy
        process = Pool(processes)
        for url_title in url_titles:
            process.apply_async(self.run_task, args=(url_title, url_timeout, callback))
        process.close()
        process.join()
        self.file.logger(self.log_path, 'Done')
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