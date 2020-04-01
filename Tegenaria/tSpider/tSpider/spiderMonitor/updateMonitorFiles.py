# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.storeHtml.sshUpload import SSHUpload
from Tegenaria.tSpider.tSpider.settings import Settings

class singleSiteDto():
    def __init__(self,
                 sitename=None,
                 ycount=None,
                 tcount=None,
                 turl=None,
                 diff=None):
        self.sitename = sitename
        self.ycount = ycount
        self.tcount = tcount
        self.turl = turl
        self.diff = diff

class allSitesDto():
    def __init__(self, prd3=None, prd4=None):
        self.prd3 = prd3
        self.prd4 = prd4

class UpdateMonitorFiles():
    def __init__(self, siteinfo=None):
        self.siteinfo = siteinfo
        self.globalSettings = Settings()
        self.doraemon = Doraemon()
        self.getSettings()
        self.file = FileIOMiddleware()
        self.ssh = SSHUpload()

    def getSettings(self):
        self.settings = self.globalSettings.CreateSettings(self.siteinfo)
        self.work_path_prd4 = self.settings.WORK_PATH_PRD1
        self.work_path_prd3 = self.settings.WORK_PATH_PRD2
        self.content_backup_path = self.settings.FINISHED_BACKUP_PATH
        self.content_backup_post_path = self.settings.FINISHED_BACKUP_POST_PATH
        self.url_backup_path = self.settings.URL_BACKUP_PATH
        self.url_backup_post_path = self.settings.URL_BACKUP_POST_PATH
        self.monitor_site_template_path = self.globalSettings.MONITOR_SITE_TEMPLATE_PATH
        self.monitor_spiders_template_path = self.globalSettings.MONITOR_SPIDERS_TEMPLATE_PATH
        self.monitor_spiders_webserver0 = self.globalSettings.MONITOR_SPIDERS_HTML_WEBSERVER0
        self.monitor_site_webserver0 = self.globalSettings.MONITOR_SITE_HTML_WEBSERVER0
        self.spiders_html_path = self.globalSettings.STATICS_HTML_PATH
        self.monitor_site_url = self.globalSettings.MONITOR_SITE_URL

    def updateSpiders(self,
                      siteName,
                      ycount1,
                      tcount1,
                      turl1,
                      diff1,
                      ycount2,
                      tcount2,
                      turl2,
                      diff2
                      ):
        return '<tr>' + \
                    '<th align="center" valign="middle">{0}</th>'.format(siteName) + \
                    '<td align="center" valign="middle">{0}</td>'.format(ycount1) + \
                    '<td align="center" valign="middle"><a href="{0}" target="_blank">{1}</a></td>'.format(turl1, tcount1) + \
                    '<td align="center" valign="middle">{0}</td>'.format(diff1) + \
                    '<td align="center" valign="middle">{0}</td>'.format(ycount2) + \
                    '<td align="center" valign="middle"><a href="{0}" target="_blank">{1}</a></td>'.format(turl2, tcount2) + \
                    '<td align="center" valign="middle">{0}</td>'.format(diff2) + \
               '</tr>'

    def updateSite(self, number, title, url):
        return '<tr>' + \
                     '<td align="center" valign="middle">{0}</td>'.format(number) + \
                     '<td align="center" valign="middle"><a href="{0}" target="_blank">{1}</a></td>'.format(url, title) + \
               '</tr>'

    def uploadFile(self, fromFile, toFile):
        while os.path.exists(fromFile):
            try:
                if self.ssh.start(self.globalSettings.IP_WEBSERVER0,
                                  self.globalSettings.PORT_WEBSERVER0,
                                  self.globalSettings.USER_ROOT_WEBSERVER0,
                                  self.globalSettings.USER_ROOT_PASSWORD_WEBSERVER0,
                                  fromFile,
                                  toFile) == True:
                    print 'Success to retry to upload monitor file: {0}'.format(fromFile)
                    os.remove(fromFile)
                    print 'Success to retry to remove monitor file: {0}'.format(fromFile)
            except Exception as e:
                print 'Exception {0} to upload monitor site file: {1}'.format(e.message, fromFile)

    def updateSingleSite(self,
                         preBackupPath,
                         postBackupPath,
                         siteName,
                         siteWorkPath,
                         remoteFilePath):
        singleSiteData = singleSiteDto(self.siteinfo.name, 0, 0, None, 0)
        isPreBackupFileExists = os.path.exists(preBackupPath)
        isPostBackupFileExists = os.path.exists(postBackupPath)
        preCsvContent = None
        if isPreBackupFileExists:
            print "Start to read url back up file: {0}".format(self.settings.NAME)
            preCsvContent = self.file.readColsFromCSV(preBackupPath, ['title', 'url'])
            singleSiteData.tcount = len(preCsvContent.values)
        else:
            print "Url back up file not exits: {0}".format(self.settings.NAME)
            singleSiteData.tcount = 0

        if isPostBackupFileExists:
            print "Start to read post url back up file: {0}".format(self.settings.NAME)
            postCsvContent = self.file.readColsFromCSV(postBackupPath, ['title', 'url'])
            singleSiteData.ycount = len(postCsvContent.values)
        else:
            print "Post url back up file not exits: {0}".format(self.settings.NAME)
            singleSiteData.ycount = 0
        singleSiteData.diff = singleSiteData.tcount - singleSiteData.ycount
        if self.doraemon.isEmpty(preCsvContent) is False:
            if preCsvContent.empty:
                print "No new back up url: {0}".format(self.settings.NAME)
            else:
                template = self.file.readFromTxt(self.monitor_site_template_path)
                finalContent = ''
                number = 1
                for item in preCsvContent.values:
                    finalContent = "{0}{1}".format(finalContent, self.updateSite(number, item[1], item[0]))
                    number += 1
                template = template.replace('UpdateTime', self.doraemon.getCurrentLocalTime())
                template = template.replace('ServerName', siteName)
                template = template.replace('SiteName', self.siteinfo.name)
                template = template.replace('MainContent', finalContent)
                turl = '{0}{1}_{2}.html'.format(self.monitor_site_url, self.settings.NAME, siteName)
                singleSiteData.turl = turl
                singleSiteHtmlPath = '{0}//{1}_{2}.html'.format(siteWorkPath, self.settings.NAME, siteName)
                self.file.writeToHtmlCover(singleSiteHtmlPath, template)
                self.uploadFile(singleSiteHtmlPath, remoteFilePath)
        return singleSiteData

    def processAllSites(self, allSitesData=None):
        template = self.file.readFromTxt(self.monitor_spiders_template_path)
        mainContent = ''
        for data in allSitesData:
            mainContent = '{0}{1}'.format(mainContent,self.updateSpiders(data.prd3.sitename,
                                                                         data.prd3.ycount,
                                                                         data.prd3.tcount,
                                                                         data.prd3.turl,
                                                                         data.prd3.diff,
                                                                         data.prd4.ycount,
                                                                         data.prd4.tcount,
                                                                         data.prd4.turl,
                                                                         data.prd4.diff))
        template = template.replace('UpdateTime', self.doraemon.getCurrentLocalTime())
        template = template.replace('MainContent', mainContent)
        self.file.writeToHtmlCover(self.spiders_html_path, template)
        self.uploadFile(self.spiders_html_path, '{0}/index.html'.format(self.monitor_spiders_webserver0))

    def processSingleSite(self):
        spidersContent = allSitesDto(None, None)
        spidersContent.prd3 = self.updateSingleSite(self.url_backup_path,
                                                    self.url_backup_post_path,
                                                    'prd3',
                                                    self.work_path_prd3,
                                                    '{0}/{1}_prd3.html'.format(self.monitor_site_webserver0,
                                                                               self.settings.NAME))
        spidersContent.prd4 = self.updateSingleSite(self.content_backup_path,
                                                    self.content_backup_post_path,
                                                    'prd4',
                                                    self.work_path_prd4,
                                                    '{0}/{1}_prd4.html'.format(self.monitor_site_webserver0,
                                                                               self.settings.NAME))
        return spidersContent

if __name__ == '__main__':
    updateMonitorFiles=UpdateMonitorFiles()
    updateMonitorFiles.startUpdateSite()