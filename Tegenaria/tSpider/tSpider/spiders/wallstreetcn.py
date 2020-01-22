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
        self.spiderBone = SpiderBone('wallstreetcn', callback=self.parse)

    def parse(self, current_url, html):
        data = None
        valid = str(filter(str.isdigit, current_url))
        if len(valid) == 0:
            print 'Invalid url: {0}'.format(current_url)
            return
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _]', current_url)
        current_id = short_url_parts[len(short_url_parts) - 1]
        not_fnd = html.xpath(".//article")

        url = ""
        content = ""
        time = ""
        author_name = ""
        title = ""
        id = ""
        if len(not_fnd) > 0:
            article_0 = html.xpath(".//*[contains(@class,'box_left')]")
            article_1 = html.xpath(".//*[contains(@class,'xiangxi')]")
            article_2 = html.xpath(".//*[contains(@class,'main')]")
            if len(article_0) > 0 and len(article_1) == 0:
                content0_1 = html.xpath(".//div[contains(@class, 'txt_con')]//p//text()")
                time0_1 = html.xpath(".//*[contains(@class, 'info')]/text()")
                title0_1 = html.xpath(".//*[contains(@class,'intal_tit')]/h2/text()")
                author_name0_1 = self.spiderBone.name
                author_name0_2 = self.spiderBone.name

                url = current_url
                id = current_id
                if self.doraemon.isEmpty(content0_1) is False:
                    content = ''.join(content0_1).strip()
                if self.doraemon.isEmpty(time0_1) is False:
                    time = ''.join(time0_1[0]).strip()
                    time = self.doraemon.getDateFromString(time)
                if self.doraemon.isEmpty(author_name0_1) is False:
                    author_name = author_name0_1
                if self.doraemon.isEmpty(author_name0_2) is False:
                    author_name = author_name0_2
                if self.doraemon.isEmpty(title0_1) is False:
                    title = title0_1[0].strip()

                data = self.doraemon.createSpiderData(url.strip(),
                                                      time.strip(),
                                                      author_name.strip(),
                                                      title.strip(),
                                                      id.strip(),
                                                      self.spiderBone.today,
                                                      self.spiderBone.source,
                                                      [],
                                                      self.spiderBone.is_open_cache,
                                                      content)

            if len(article_1) > 0:
                content1_1 = html.xpath(".//div[contains(@class, 'txt_con')]/p/text()")
                time1_1 = ""
                author_name1_1= self.spiderBone.name
                title1_1 = html.xpath(".//*[contains(@class,'xiangxi')]/h2/text()")

                url = current_url
                id = current_id

                if self.doraemon.isEmpty(content1_1) is False:
                    content = ''.join(content1_1).strip()
                if self.doraemon.isEmpty(time1_1) is False:
                    time = ''.join(time1_1[0]).strip()
                    time = self.doraemon.getDateFromString(time)
                if self.doraemon.isEmpty(author_name1_1) is False:
                    author_name = author_name1_1
                if self.doraemon.isEmpty(title1_1) is False:
                    title = title1_1[0].strip()

                data = self.doraemon.createSpiderData(url.strip(),
                                                      time.strip(),
                                                      author_name.strip(),
                                                      title.strip(),
                                                      id.strip(),
                                                      self.spiderBone.today,
                                                      self.spiderBone.source,
                                                      [],
                                                      self.spiderBone.is_open_cache,
                                                      content)

            if len(article_2) > 0:
                time2_1 = html.xpath(".//*[contains(@class, 'meta-item time')]/text()")
                content2_1 = html.xpath(".//*[contains(@class, 'rich-text')]/p/text()")
                author2_1 = self.spiderBone.name
                title2_1 = html.xpath(".//*[contains(@class,'article-header')]/h1/text()")

                url = current_url
                id = current_id

                if self.doraemon.isEmpty(content2_1) is False:
                    content = ''.join(content2_1).strip()
                if self.doraemon.isEmpty(time2_1) is False:
                    time = ''.join(time2_1[0]).strip()
                    time = self.doraemon.getDateFromString(time)
                if self.doraemon.isEmpty(author2_1) is False:
                    author_name = author2_1
                if self.doraemon.isEmpty(title2_1) is False:
                    title = title2_1[0].strip()

                data = self.doraemon.createSpiderData(url.strip(),
                                                      time.strip(),
                                                      author_name.strip(),
                                                      title.strip(),
                                                      id.strip(),
                                                      self.spiderBone.today,
                                                      self.spiderBone.source,
                                                      [],
                                                      self.spiderBone.is_open_cache,
                                                      content)
        return data

if __name__ == '__main__':
    spider=Spider()
    spider.spiderBone.start()