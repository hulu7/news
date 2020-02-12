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
        self.spiderBone = SpiderBone('engadget', callback=self.parse)
        self.regx = re.compile("(http(s?):)?\/\/cn\.engadget\.com\/cn\-[0-9a-z\-]{0,}\.html")

    def parse(self, current_url, html):
        data = None
        isValid = self.regx.match(current_url) != None
        if isValid is False:
            print 'Invalid url: {0}'.format(current_url)
            return data
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _, %, ?, =, &"]', current_url)
        current_id = short_url_parts[short_url_parts.index('engadget') + 2]
        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        article_0 = html.xpath(".//*[contains(@class, 'rwd-inner-container W(1235px) W(980px)--lg W(100%)--md Mx(20px)--md D(f) Ai(st) My(40px) Miw(0)')]")
        if len(article_0) > 0:
            content0_1 = article_0[0].xpath(".//*[contains(@data-testid, 'PostContentContainer')]//div//text()")
            time0_1 = article_0[0].xpath(".//*[contains(@class, 'Mt(5px) C(engadgetFontLightGray)')]//text()")
            author_name0_1 = self.spiderBone.name
            title0_1 = article_0[0].xpath(".//*[contains(@class, 'Ff($ff-primary) M(0) C(engadgetBlack) Fw(400) Fz(36px) Mt(10px) Fz(48px)! Lh(55px) Fz(24px)!--sm Lh(n)--sm')]//text()")
            images0_1 = article_0[0].xpath(".//*[contains(@data-testid, 'PostContentContainer')]//img/@src")

            url = current_url
            id = current_id
            if self.doraemon.isEmpty(content0_1) is False:
                content += ''.join(content0_1).strip()
            if self.doraemon.isEmpty(time0_1) is False:
                time = ''.join(time0_1).strip().replace('\n', '')
                time = self.doraemon.getDateFromString(time)
            if self.doraemon.isEmpty(author_name0_1) is False:
                author_name = author_name0_1
            if self.doraemon.isEmpty(title0_1) is False:
                title = ''.join(title0_1[0]).strip()
            images = []
            self.doraemon.updateImages(images, images0_1)

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