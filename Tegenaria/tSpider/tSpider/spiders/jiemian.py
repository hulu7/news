# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urlparse
import re
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.spiderBone import SpiderBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Spider():
    def __init__(self):
        self.doraemon = Doraemon()
        self.spiderBone = SpiderBone('jiemian', callback=self.parse)

    def parse(self, current_url, html):
        data = None
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _, -]', current_url)
        current_id = short_url_parts[len(short_url_parts) - 2]
        article_content = html.xpath(".//*[contains(@class,'article-view')]")

        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(article_content) > 0:
            article_0 = html.xpath(".//*[contains(@class,'article-view')]")
            if len(article_0) > 0:
                content0_1 = html.xpath(".//*[contains(@class, 'article-main')]//p//text()")
                time0_1 = html.xpath(".//*[contains(@class, 'article-info')]//*//span//text()")
                author_name0_1 = self.spiderBone.name
                title0_1 = html.xpath(".//*[contains(@class,'article-header')]/h1/text()")
                images0_1 = html.xpath(".//*[contains(@class,'article-main')]//*//img//@src")

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.doraemon.isEmpty(time0_1) is False:
                    time = ''.join(time0_1).strip()
                    time = self.doraemon.getDateFromString(time)
                if self.doraemon.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1
                if self.doraemon.isEmpty(title0_1) is False:
                    title = title0_1[0].strip()

                images = []
                self.doraemon.updateImages(images, images0_1)
                images_src = []
                for image in images:
                    images_src.append(urlparse.urljoin(current_url, image))

                data = self.doraemon.createSpiderData(url.strip(),
                                                      time.strip(),
                                                      author_name.strip(),
                                                      title.strip(),
                                                      id.strip(),
                                                      self.spiderBone.today,
                                                      self.spiderBone.source,
                                                      images_src,
                                                      self.spiderBone.is_open_cache,
                                                      content)
        return data

if __name__ == '__main__':
    spider=Spider()
    spider.spiderBone.start()