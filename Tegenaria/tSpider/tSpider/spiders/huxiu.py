#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.spiderBone import SpiderBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Spider():
    def __init__(self):
        self.doraemon = Doraemon()
        self.spiderBone = SpiderBone('huxiu', callback=self.parse)
        self.time = time

    def parse(self, current_url, html):
        data = None
        print 'Start to parse: {0}'.format(current_url)

        title = ""
        url = ""
        id = ""
        image_url = ""
        content = ""
        time = ""
        author_name = ""
        valid = False

        url = current_url
        id = str(filter(str.isdigit, current_url.encode('gbk')))
        title1 = html.xpath(".//*[contains(@class,'article__title')]/text()")
        content1 = html.xpath(".//*[contains(@class, 'article__content')]//*//text()")
        time1 = html.xpath(".//*[contains(@class, 'article__time')]/text()")
        author_url1 = html.xpath(".//*[contains(@class, 'author-info__username')]//text()")
        author_name1 = self.spiderBone.name
        images0_1 = html.xpath(".//*[contains(@class,'top-img')]//img//@src")
        images0_2 = html.xpath(".//*[contains(@class,'img-center-box')]//img//@src")
        self.time.sleep(2)
        if self.doraemon.isEmpty(title1) is False:
            title = title1[0].strip()
        if self.doraemon.isEmpty(content1) is False:
            content = ''.join(content1).strip()
            valid = True
        if self.doraemon.isEmpty(time1) is False:
            time = ''.join(time1).strip()
            time = self.doraemon.getDateFromString(time)
        if self.doraemon.isEmpty(author_url1) is False:
            author_url = author_url1[0].strip()
        if self.doraemon.isEmpty(author_name1) is False:
            author_name = author_name1

        images = []
        images0_1 = self.doraemon.completeImageUrls(images0_1, url)
        images0_2 = self.doraemon.completeImageUrls(images0_2, url)
        self.doraemon.updateImages(images, images0_1)
        self.doraemon.updateImages(images, images0_2)

        data = self.doraemon.createSpiderData(url.strip(),
                                              time.strip(),
                                              author_name.strip(),
                                              title.strip(),
                                              id.strip(),
                                              self.spiderBone.today,
                                              self.spiderBone.source,
                                              images,
                                              self.spiderBone.is_open_cache,
                                              content)

        return data

if __name__ == '__main__':
    spider=Spider()
    spider.spiderBone.start()