# -*- coding: utf-8 -*-
from lxml import etree
class Test():

    def __init__(self):
        self.html_path = '/home/dev/Data/html.txt'

    def test(self):
        with open(self.html_path, 'r') as txt_file:
            txt = txt_file.read()
        txt_file.close()
        html = etree.HTML(txt)
        print 'pass 1 html: {0}'.format(html)
        href_items = html.xpath(".//a")
        print 'pass 1 href_items: {0}'.format(len(href_items))
        end = 0


if __name__ == '__main__':
    test=Test()
    test.test()