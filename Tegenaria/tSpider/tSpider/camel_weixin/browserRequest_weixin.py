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
import time
from middlewares.fileIOMiddleware import FileIOMiddleware
from seleniumMiddleware_weixin import SeleniumMiddleware

class BrowserRequest():
    def run_task(self, url_title, callback=callable):
        self.file.logger(self.log_path, 'Start: {0}'.format(url_title[0]))
        print 'Start: {0}'.format(url_title[0])
        request = SeleniumMiddleware()
        request.chrome_request('https://weixin.sogou.com/', self.log_path, self.proxy)
        time.sleep(3)
        input = request.browser.find_element_by_id("query")
        input.send_keys(url_title[0])
        button = request.browser.find_element_by_class_name("swz2")
        button.click()
        time.sleep(2)
        if self.is_blocked(request.browser):
            print 'The ip: {0} is blocked.'.format(self.proxy)
            request.browser.close()
            request.browser.quit()
            del request.browser
            gc.collect()
            response = []
        else:
            account = request.browser.find_element_by_xpath("//a[@uigs='account_name_0']")
            account.click()
            time.sleep(2)
            request.browser.switch_to_window(request.browser.window_handles[1])
            response = request.browser
        try:
            callback({'response': response, 'request_url': url_title[0], 'request_title': url_title[1]})
        except Exception as e:
            self.file.logger(self.log_path, 'Exception: {0} for {1}'.format(e.message, url_title[0]))
            print 'Exception: {0} for {1}'.format(e.message, url_title[0])
            request.browser.close()
            request.browser.quit()
            del request
            gc.collect()
        self.content.append({'current_url': response.current_url, 'page_source': response.page_source})
        self.file.logger(self.log_path, 'End: {0}'.format(response.current_url))
        print 'End: {0}'.format(response.current_url)
        response.close()
        response.quit()
        del response, request
        gc.collect()

    def is_blocked(self, browser):
        try:
            browser.find_element_by_id("seccodeImage")
            return True
        except:
            return False

    def start_chrome(self, url_titles, processes, log_path, proxy, callback=callable):
        self.file = FileIOMiddleware()
        self.content = []
        self.log_path = log_path
        self.proxy = proxy
        process = Pool(processes)
        for url_title in url_titles:
            process.apply_async(self.run_task, args=(url_title, callback))
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