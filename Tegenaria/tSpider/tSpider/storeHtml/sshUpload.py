# -*- coding:utf-8 -*-
import sys
reload(sys)
import os
import re
sys.path.append("/home/dev/Repository/news/")
from Tegenaria.tSpider.tSpider.settings import Settings
from Tegenaria.tSpider.tSpider.middlewares.fileIOMiddleware import FileIOMiddleware
from Tegenaria.tSpider.tSpider.middlewares.doraemonMiddleware import Doraemon

class SSHUpload():
    def __init__(self):
        self.settings = Settings()
        self.file = FileIOMiddleware()
        self.doraemon = Doraemon()

    def writeBack(self, fromFiles):
        print "Start to update retry file: {0}".format(self.settings.RETRY_FILE)
        writeBackContent = ''
        for file in fromFiles:
            writeBackContent = '{0}{1}\n'.format(writeBackContent, file)
        self.file.writeToTxtAdd(self.settings.RETRY_FILE, writeBackContent)
        print "Finished to update retry file: {0}".format(self.settings.RETRY_FILE)

    def updateRemoveFile(self, fromFiles):
        if self.doraemon.isEmpty(fromFiles):
            print "No need to update to remove retry file."
            return
        content = self.readFile()
        print "Start to delete retry file: {0}".format(self.settings.RETRY_FILE)
        os.remove(self.settings.RETRY_FILE)
        print "Finished to delete retry file: {0}".format(self.settings.RETRY_FILE)
        for file in fromFiles:
            if file in content:
                del content[content.index(file)]
            else:
                content.append(file)
        self.writeBack(content)

    def updateAddFile(self, fromFiles):
        if self.doraemon.isEmpty(fromFiles):
            print "No need to update to add retry file"
            return
        content = self.readFile()
        if self.doraemon.isEmpty(content):
            self.writeBack(fromFiles)
            return
        print "Start to delete retry file: {0}".format(self.settings.RETRY_FILE)
        os.remove(self.settings.RETRY_FILE)
        print "Finished to delete retry file: {0}".format(self.settings.RETRY_FILE)
        for file in content:
            if file not in fromFiles:
                fromFiles.append(file)
        self.writeBack(fromFiles)

    def readFile(self):
        files = []
        isRetryFileExists = os.path.exists(self.settings.RETRY_FILE)
        if isRetryFileExists == False:
            return files
        content = self.file.readFromTxt(self.settings.RETRY_FILE)
        if self.doraemon.isEmpty(content):
            return files
        items = content.split('\n')
        for item in items:
            if self.doraemon.isEmpty(item):
                continue
            files.append(item)
        return files

    def retry(self):
        while True:
            files = self.readFile()
            updateFiles = []
            try:
                for fromFile in files:
                    fileParts = re.split(r'[/]', fromFile)
                    fileName = fileParts[len(fileParts) - 1]
                    toFile = '{0}/{1}'.format(self.settings.HTML_WEBSERVER0, fileName)
                    if self.doraemon.sshUpload(self.settings.IP_WEBSERVER0,
                                               self.settings.PORT_WEBSERVER0,
                                               self.settings.USER_ROOT_WEBSERVER0,
                                               self.settings.USER_ROOT_PASSWORD_WEBSERVER0,
                                               fromFile,
                                               toFile):
                        updateFiles.append(fromFile)
                        print 'Success to retry to upload: {0}'.format(fromFile)
                self.updateRemoveFile(updateFiles)
            except Exception as e:
                self.updateRemoveFile(updateFiles)
                print 'Exception {0} to retry to upload: {1}'.format(e.message, fromFile)

    def startUpload(self):
        fromFile = '{0}.tar.gz'.format(self.settings.LOCAL_HTML_PATH)
        if not os.listdir(self.settings.LOCAL_HTML_PATH) and os.path.exists(fromFile) is False:
            print 'no html file to tar'
            return
        uploadedList = []
        if os.path.exists(fromFile) is False:
            uploadedList = self.doraemon.tarList(self.settings.LOCAL_HTML_PATH)
        while os.path.exists(fromFile):
            try:
                if self.doraemon.uploadFileApi(self.settings.UPLOAD_HTML_API,
                                               'local.tar.gz',
                                               fromFile):
                    os.remove(fromFile)
                    for file in uploadedList:
                        self.doraemon.deleteFile(file)
                    print 'Success to upload html file: {0}'.format(fromFile)
            except Exception as e:
                print 'Exception {0} to upload html file: {1}'.format(e.message, fromFile)

if __name__ == '__main__':
    sshUpload=SSHUpload()
    sshUpload.startUpload()