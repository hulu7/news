# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.spiderBone import SpiderBone
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class Spider():
    def __init__(self, siteinfo=None):
        self.siteinfo = siteinfo
        if self.siteinfo == None:
            return
        self.doraemon = Doraemon()
        self.spiderBone = SpiderBone(self.siteinfo, callback=self.parse)
        self.regx = self.siteinfo.content_url_match
        self.content_id_tag = self.siteinfo.content_id_tag
        self.article_match = self.siteinfo.article_match
        self.content_match = self.siteinfo.content_match
        self.content_time_match = self.siteinfo.content_time_match
        self.content_title_match = self.siteinfo.content_title_match
        self.content_image_match = self.siteinfo.content_image_match

    def parse(self, current_url, html):
        data = None
        isValid = False
        for rule in self.regx:
            isValid = rule.match(current_url) != None
            if isValid:
                break
        if isValid is False:
            print 'Invalid url: {0}'.format(current_url)
            return data
        print 'Start to parse: {0}'.format(current_url)
        short_url_parts = re.split(r'[., /, _, %, ?, =, &"]', current_url)
        id = self.doraemon.getUrlId(short_url_parts, self.content_id_tag)
        url = current_url
        author_name = self.spiderBone.name
        content = ""
        time = ""
        title = ""
        for article_rule in self.article_match:
            article = html.xpath('{0}'.format(article_rule.regx))
            if self.doraemon.isEmpty(article) is False:
                article_child = self.doraemon.getMatchContent(article, article_rule)
                images = []
                for content_rule in self.content_match:
                    content_tmp = article_child.xpath('{0}'.format(content_rule.regx))
                    content_child = self.doraemon.getMatchContent(content_tmp, content_rule)
                    if self.doraemon.isEmpty(content_child) is False:
                        content += ''.join(content_child).strip()
                        break
                for time_rule in self.content_time_match:
                    if time_rule.index == -2:
                        time = self.spiderBone.today
                        break
                    time_tmp = article_child.xpath('{0}'.format(time_rule.regx))
                    time_child = self.doraemon.getMatchContent(time_tmp, time_rule)
                    if self.doraemon.isEmpty(time_child) is False:
                        time = ''.join(time_child).strip().replace('\n', '')
                        time = self.doraemon.getDateFromString(time)
                        break
                for title_rule in self.content_title_match:
                    title_tmp = article_child.xpath('{0}'.format(title_rule.regx))
                    title_child = self.doraemon.getMatchContent(title_tmp, title_rule)
                    if self.doraemon.isEmpty(title_child) is False:
                        title = ''.join(title_child).strip()
                        break
                for image_rule in self.content_image_match:
                    if image_rule.index == -2:
                        continue
                    images_tmp = article_child.xpath('{0}'.format(image_rule.regx))
                    images_child = self.doraemon.getMatchContent(images_tmp, image_rule)
                    if images_child != None:
                        self.doraemon.updateImages(images, images_child)
                images = self.doraemon.completeImageUrls(images, current_url)
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