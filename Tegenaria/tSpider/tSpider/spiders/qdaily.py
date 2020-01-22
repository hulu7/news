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
        self.spiderBone = SpiderBone('qdaily', callback=self.parse)

    def parse(self, current_url, html):
        data = None
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _, %, "]', current_url)
        current_id = short_url_parts[short_url_parts.index('articles') + 1]
        article_content = html.xpath(".//*[contains(@class, 'main')]")

        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(article_content) > 0:
            article_0 = html.xpath(".//*[contains(@class, 'main')]")
            if len(article_0) > 0:
                content0_1 = html.xpath(".//*[contains(@class, 'detail')]//p//text()")
                time0_1 = html.xpath(".//*[contains(@class, 'date smart-date')]/text()")
                author_name0_1 = self.spiderBone.name
                title0_1 = html.xpath(".//*[contains(@class, 'media-title')]/h2/text()")
                title0_2 = html.xpath(".//*[contains(@class, 'category-title')]/h2/text()")
                images0_1 = html.xpath(".//*[contains(@class, 'full-banner-bd imgcover')]//img//@src")
                images0_2 = html.xpath(".//*[contains(@class, 'article-detail-hd')]//img//@src")
                images0_3 = html.xpath(".//*[contains(@class, 'detail')]//figure//img//@data-src")


                url = current_url
                id = current_id
                if self.doraemon.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.doraemon.isEmpty(time0_1) is False:
                    time = ''.join(time0_1).strip()
                    time = time.replace(' ', '')
                    time = self.doraemon.getDateFromString(time)
                if self.doraemon.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1
                if self.doraemon.isEmpty(title0_1) is False:
                    title = ''.join(title0_1).strip()
                if self.doraemon.isEmpty(title0_2) is False:
                    title = ''.join(title0_2).strip()

                images = []
                images0_1 = self.doraemon.completeImageUrls(images0_1, url)
                images0_2 = self.doraemon.completeImageUrls(images0_2, url)
                images0_3 = self.doraemon.completeImageUrls(images0_3, url)
                self.doraemon.updateImages(images, images0_1)
                self.doraemon.updateImages(images, images0_2)
                self.doraemon.updateImages(images, images0_3)

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