# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.spiderBone import SpiderBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Spider():
    def __init__(self):
        self.doraemon = Doraemon()
        self.spiderBone = SpiderBone('tmtpost', callback=self.parse)

    def parse(self, current_url, html):
        data = None
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _, %, "]', current_url)
        current_id = short_url_parts[len(short_url_parts) - 2]
        article_content = html.xpath(".//article")

        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(article_content) > 0:
            article_0 = html.xpath(".//article")
            if len(article_0) > 0:
                content0_1 = html.xpath(".//*[contains(@class, 'inner')]//p//text()")
                time0_1 = html.xpath(".//*[contains(@class, 'time ')]/text()")
                author_name0_1 = self.spiderBone.name
                title0_1 = html.xpath(".//article/h1/text()")
                images0_1 = html.xpath(".//*[contains(@class, 'inner')]//p//img//@src")
                images0_2 = html.xpath(".//*[contains(@class, 'inner')]//div//img//@src")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.doraemon.isEmpty(time0_1) is False:
                    time = ''.join(time0_1[0]).strip()
                    time = self.doraemon.getDateFromString(time)
                if self.doraemon.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1
                if self.doraemon.isEmpty(title0_1) is False:
                    title = ''.join(title0_1[0]).strip()

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