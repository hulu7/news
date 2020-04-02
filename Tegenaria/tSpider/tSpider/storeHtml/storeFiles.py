# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import copy
from PIL import Image
import re
import urlparse
from bs4 import BeautifulSoup
from bs4.element import NavigableString
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.storeHtml.aliyunUpload import AliUpload
from Tegenaria.tSpider.tSpider.storeHtml.sshUpload import SSHUpload

class matchRules():
    def __init__(self, tag=None, key=None, value=None):
        self.tag = tag
        self.key = key
        self.value = value

class imgInfo():
    def __init__(self, src=None, width=None, height=None):
        self.src = src
        self.width = width
        self.height = height
        self.dataRatio = 0.567

class updateNode():
    def __init__(self, isImageNode=False, node=None, imageOriginUrl=None, imageNewUrl=None):
        self.isImageNode = isImageNode
        self.node = node
        self.imageOriginUrl = imageOriginUrl
        self.imageNewUrl = imageNewUrl

class StoreFiles():
    def __init__(self,
                 htmlpath=None,
                 imagepath=None,
                 templatepath=None,
                 articleurl=None,
                 alidomain=None,
                 alidomaindeepinews=None,
                 alidomaindeepinewsimg=None,
                 ipwebserver0=None,
                 portwebserver0=None,
                 userrootwebserver0=None,
                 userrootpasswordwebserver0=None,
                 htmlwebserver0=None,
                 needselfimage=None,
                 needselfhtml=None):
        self.doraemon = Doraemon()
        self.file = FileIOMiddleware()
        self.image_count = 0
        self.htmlpath = htmlpath
        self.imagepath = imagepath
        self.templatepath = templatepath
        self.articleurl = articleurl
        self.alidomain = alidomain
        self.alidomaindeepinews = alidomaindeepinews
        self.alidomaindeepinewsimg = alidomaindeepinewsimg
        self.ipwebserver0 = ipwebserver0
        self.portwebserver0 = portwebserver0
        self.userrootwebserver0 = userrootwebserver0
        self.userrootpasswordwebserver0 = userrootpasswordwebserver0
        self.htmlwebserver0 = htmlwebserver0
        self.needselfimage = needselfimage
        self.needselfhtml = needselfhtml

    def parseContentRegxRule(self, content_regx_rule):
        result = matchRules(None, None, None)
        rules = [matchRules(r'[\.][\/][\/](.*?)[[]', r'[\@](.*?)[\=]', r'[\'](.*?)[\']'),
                 matchRules(r'[\.][\/][\/](.*?)[[]', r'[\@](.*?)[,]', r'[\'](.*?)[\']'),
                ]
        for rule in rules:
            tag = re.findall(rule.tag, content_regx_rule)
            key = re.findall(rule.key, content_regx_rule)
            value = re.findall(rule.value, content_regx_rule)
            if self.doraemon.isEmpty(tag) is False and \
               self.doraemon.isEmpty(key) is False and \
               self.doraemon.isEmpty(value) is False:
                result.tag = tag[0]
                result.key = key[0]
                result.value = value[0]
                break
        return result

    def addHighlightTextInner(self, content):
        return '<strong class="article_paragraph_border">{0}</strong>'.format(content) + \
               '<p class="article_paragraph">' + \
                    '<br class="article_paragraph_border"/>' + \
               '</p>'

    def addHighlightTextOuter(self, node, content):
        return '{0}<p class="article_paragraph">'.format(node) + \
                      '<strong class="article_paragraph_border">{0}</strong>'.format(content) + \
                  '</p>' + \
                  '<p class="article_paragraph">' + \
                      '<br class="article_paragraph_border"/>' + \
                  '</p>'

    def addImgNode(self, node, dataSrc, dataRef, width, dataRatio):
        if width == None:
            width = 1000
        return '{0}<p class="article_paragraph_imag">'.format(node) + \
                      '<img data-ratio="{0}"'.format(dataRatio) + \
                           'data-src="{0}"'.format(dataSrc) + \
                           'data-ref="{0}"'.format(dataRef) + \
                           'data-type="jpeg"' + \
                           'data-w={0} '.format(width) + \
                           'class="article_paragraph_img"/>' + \
                  '</p>' + \
                  '<p class="article_paragraph">' + \
                     '<br class="article_paragraph_border"/>' + \
                  '</p>'

    def addTextNodeOuter(self, node, content):
        if self.doraemon.isEmpty(content):
            return ''
        return '{0}<p class="article_paragraph">{1}'.format(node, content) + \
                  '</p>' + \
                  '<p class="article_paragraph">' + \
                      '<br class="article_paragraph_border"/>' + \
                  '</p>'

    def addParagraphGapNode(self, node):
        return '{0}<p class="article_paragraph">'.format(node) + \
                     '<br class="article_paragraph_border"/>' + \
                  '</p>'

    def addH1Node(self, node, content):
        return '{0}<p label="h1" class="article_paragraph_h1">'.format(node) + \
                    '<span class="article_paragraph_h1_1">' + \
                        '<span class="article_paragraph_h1_1_1">' + \
                            '<span class="article_paragraph_h1_1_1_1">{0}'.format(content) + \
                            '</span>' + \
                        '</span>' + \
                    '</span>' + \
                  '</p>' + \
                  '<p class="article_paragraph">' + \
                     '<br class="article_paragraph_border"/>' + \
                  '</p>'

    def extractImgSize(self, style, mode):
        size = re.findall(r'{0}:(.*?)px;'.format(mode), style)
        if len(size) == 1:
            return size[0].strip()
        return None

    def extractImg(self, url, node):
        result = imgInfo(None, None, None)
        if isinstance(node, NavigableString):
            return None
        if node.name != 'img' and len(node.contents) == 0:
            return result
        if node.name == 'img':
            if node.attrs.has_key('src') and self.doraemon.isEmpty(result.src):
                if 'data:image/' not in node.attrs['src']:
                    result.src = node.attrs['src']
            if node.attrs.has_key('_src') and self.doraemon.isEmpty(result.src):
                if 'data:image/' not in node.attrs['_src']:
                    result.src = node.attrs['_src']
            if node.attrs.has_key('data-original') and self.doraemon.isEmpty(result.src):
                if 'data:image/' not in node.attrs['data-original']:
                    result.src = node.attrs['data-original']
            if node.attrs.has_key('data-src') and self.doraemon.isEmpty(result.src):
                if 'data:image/' not in node.attrs['data-src']:
                    result.src = node.attrs['data-src']
            if node.attrs.has_key('data-lazy-src') and self.doraemon.isEmpty(result.src):
                if 'data:image/' not in node.attrs['data-lazy-src']:
                    result.src = node.attrs['data-lazy-src']
            if node.attrs.has_key('width') and result.width == None:
                result.width = node.attrs['width']
            if node.attrs.has_key('height') and result.height == None:
                result.height = node.attrs['height']
            if node.attrs.has_key('data-w') and result.width == None:
                result.width = node.attrs['data-w']
            if node.attrs.has_key('data-h') and result.height == None:
                result.height = node.attrs['data-h']
            if node.attrs.has_key('data-backh') and result.height == None:
                result.height = node.attrs['data-backh']
            if node.attrs.has_key('data-backw') and result.width == None:
                result.width = node.attrs['data-backw']
            if node.attrs.has_key('data-wscnh') and result.height == None:
                result.height = node.attrs['data-wscnh']
            if node.attrs.has_key('data-wscnw') and result.width == None:
                result.width = node.attrs['data-wscnw']
            if node.attrs.has_key('style') and (result.width == None or result.height == None):
                result.width = self.extractImgSize(node.attrs['style'], 'width')
                result.height = self.extractImgSize(node.attrs['style'], 'height')
            if isinstance(result.width, int) and isinstance(result.height, int):
                result.dataRatio = float(float(result.height) / float(result.width))
            if result.src != None:
                result.src = urlparse.urljoin(url, result.src).strip()
            return result
        if len(node.contents) > 0:
            for n in node.contents:
                result = self.extractImg(url, n)
                if result != None:
                    return result
        return result

    def nodeTraversal(self, url, node, newNode, articleId):
        if node.name == 'strong' and \
           node.parent.name == 'div' and \
           self.doraemon.isEmpty(node.string) is False:
            newNode = '{0}{1}'.format(newNode, self.addHighlightTextOuter(newNode, node.string))
        if (node.name == 'h1' or \
           node.name == 'h2' or \
           node.name == 'h3' or \
           node.name == 'h4') and \
           self.doraemon.isEmpty(node.string) is False:
           newNode = '{0}{1}'.format(newNode, self.addH1Node(newNode, node.string))
        if isinstance(node, NavigableString) or \
           node.name == 'a' or \
           node.name == 'p' or \
           node.name == 'span' or \
           node.name == 'section':
           if isinstance(node, NavigableString):
                newNode = self.addTextNodeOuter(newNode, str(node))
           else:
               if self.doraemon.isEmpty(node.text) == False:
                   newNode = self.addTextNodeOuter(newNode, node.text)
        img = self.extractImg(url, node)
        updatedNode = updateNode(False, newNode, None, None)
        if img != None and img.src != None:
            updatedNode.isImageNode = True
            updatedNode.imageOriginUrl = img.src
            updatedNode.imageNewUrl = img.src
            try:
                imageType = self.doraemon.getImageTypeFromUrl(updatedNode.imageOriginUrl)
                imageId = '{0}_{1}'.format(articleId, self.image_count)
                newImageName = '{0}.{1}'.format(imageId, imageType)
                if self.doraemon.downloadImage(updatedNode.imageOriginUrl,
                                               self.imagepath,
                                               newImageName):
                    imageInfo = Image.open('{0}/{1}'.format(self.imagepath, newImageName))
                    if self.doraemon.isEmpty(imageInfo.width) is False:
                        img.width = imageInfo.width
                    if self.doraemon.isEmpty(imageInfo.height) is False:
                        img.height = imageInfo.height
                    if isinstance(img.width, int) and isinstance(img.height, int):
                        img.dataRatio = float(float(img.height) / float(img.width))
                    if self.needselfimage:
                        updatedNode.imageNewUrl = 'https://{0}.{1}/{2}/{3}'.format(self.alidomaindeepinews,
                                                                                   self.alidomain,
                                                                                   self.alidomaindeepinewsimg,
                                                                                   newImageName)
                        imageUpload = AliUpload('{0}'.format(self.imagepath),
                                                newImageName,
                                                '{0}'.format(self.alidomaindeepinews),
                                                '{0}'.format(self.alidomaindeepinewsimg))
                        if imageUpload.start():
                            updatedNode.node = '{0}{1}'.format(newNode,
                                                               self.addImgNode(newNode,
                                                                               updatedNode.imageNewUrl,
                                                                               updatedNode.imageNewUrl,
                                                                               img.width,
                                                                               img.dataRatio))
                            self.image_count += 1
                    else:
                        updatedNode.node = '{0}{1}'.format(newNode,
                                                           self.addImgNode(newNode,
                                                                           img.src,
                                                                           img.src,
                                                                           img.width,
                                                                           img.dataRatio))
                else:
                    updatedNode.node = '{0}{1}'.format(newNode,
                                                       self.addImgNode(newNode,
                                                                       img.src,
                                                                       img.src,
                                                                       img.width,
                                                                       img.dataRatio))
            except Exception as e:
                updatedNode.node = '{0}{1}'.format(newNode,
                                                   self.addImgNode(newNode,
                                                                   img.src,
                                                                   img.src,
                                                                   img.width,
                                                                   img.dataRatio))
                print 'Exception {0} to download image: {1}'.format(e.message, updatedNode.imageOriginUrl)

        return updatedNode

    def updateTemplate(self,
                       template,
                       articleHeadDescription,
                       articleHeadAuthor,
                       articleHeadTitle,
                       articleHeadOriginUrl,
                       articleBodyTitle,
                       articleBodyAuthor,
                       articleBodyPublishTime,
                       articleBodyParagraph,
                       articleBodyOriginUrl):
        template = template.replace('ArticleHeadDescription', articleHeadDescription)
        template = template.replace('ArticleHeadAuthor', articleHeadAuthor)
        template = template.replace('ArticleHeadTitle', articleHeadTitle)
        template = template.replace('ArticleHeadOriginUrl', articleHeadOriginUrl)
        template = template.replace('ArticleBodyTitle', articleBodyTitle)
        template = template.replace('ArticleBodyAuthor', articleBodyAuthor)
        template = template.replace('ArticleBodyPublishTime', articleBodyPublishTime)
        template = template.replace('ArticleBodyParagraph', articleBodyParagraph)
        template = template.replace('ArticleBodyOriginUrl', articleBodyOriginUrl)
        return template

    def hasText(self, nodes):
        for node in nodes:
            if isinstance(node, NavigableString):
                continue
            if node.name == 'img' or \
               node.name == 'a' or \
               node.name == 'p' or \
               node.name == 'span' or \
               node.name == 'section':
                return True
        return False

    def goDeepToArticleBody(self, contents):
        if isinstance(contents, NavigableString):
            return contents
        if len(contents) == 0:
            return contents
        if self.hasText(contents):
            return contents
        if len(contents) > 0:
            for n in contents:
                if isinstance(n, NavigableString):
                    continue
                return self.goDeepToArticleBody(n.contents)

    def storeFiles(self, data, page_source, content_regx_rule):
        if self.needselfhtml == False:
            return data
        try:
            self.image_count = 0
            newData = copy.copy(data)
            newArticleId = self.doraemon.getMD5('{0}_{1}'.format(data.author_name, data.id))
            newData.url = '{0}{1}.html'.format(self.articleurl, newArticleId)
            template = self.file.readFromTxt(self.templatepath)
            match = self.parseContentRegxRule(content_regx_rule)
            if match.tag is None or \
               match.key is None or \
               match.value is None:
                print 'No match rule available for html'
                return data
            soup = BeautifulSoup(page_source, 'lxml')
            matchTags = soup.select('{0}[{1}="{2}"]'.format(match.tag, match.key, match.value))
            if len(matchTags) == 0:
                print 'No tag matched for html'
                return data
            nodes = self.goDeepToArticleBody(matchTags[0].contents)
            articleContent = ''
            for node in nodes:
                if isinstance(node, NavigableString):
                    continue
                if self.doraemon.isEmpty(node):
                    continue
                newNode = ''
                updateNodeInfo = self.nodeTraversal(data.url, node, newNode, newArticleId)
                articleContent = '{0}{1}'.format(articleContent, updateNodeInfo.node)
                if updateNodeInfo.isImageNode:
                    if updateNodeInfo.imageOriginUrl in newData.images:
                        for i in newData.images:
                            if updateNodeInfo.imageOriginUrl in i or \
                               updateNodeInfo.imageOriginUrl == i:
                                newData.images[newData.images.index(i)] = updateNodeInfo.imageNewUrl
                    else:
                        newData.images.append(updateNodeInfo.imageNewUrl)
            template = self.updateTemplate(template,
                                           newData.title,
                                           '深度资讯DeepINews',
                                           newData.title,
                                           newData.url,
                                           newData.title,
                                           newData.source,
                                           newData.public_time,
                                           articleContent,
                                           data.url)
            if self.doraemon.storeHtml(newArticleId, template, self.htmlpath):
                sshUpload = SSHUpload()
                fromFile = '{0}/{1}.html'.format(self.htmlpath, newArticleId)
                if sshUpload.start(self.ipwebserver0,
                                   self.portwebserver0,
                                   self.userrootwebserver0,
                                   self.userrootpasswordwebserver0,
                                   fromFile,
                                   '{0}/{1}.html'.format(self.htmlwebserver0, newArticleId)) == False:
                    sshUpload.updateAddFile([fromFile])
            return newData
        except Exception as e:
            print 'Exception {0} when update : {1}'.format(e.message, data.url)
            return data

if __name__ == '__main__':
    storeFiles=StoreFiles()
    storeFiles.parse()