#coding:utf-8
#------requirement------
#pymongo-3.7.1
#------requirement------
import os
import shutil
import sys
import time
import tarfile
reload(sys)
sys.setdefaultencoding('utf-8')

class UpdateHtml():
    def __init__(self):
        self.today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self.path = '/home/dev/Data/Production/local.tar.gz'
        self.articlePath = '/home/dev/Data/Production/article'
        self.logpath = '/home/dev/Data/Log/{0}_log.log'.format(self.today)

    def writeToTxtAdd(self, file_path, content):
        with open(file_path, 'a') as txt_writer:
            txt_writer.write(str(content) + '\n')
        txt_writer.close()

    def logger(self, file_path, content):
        local_time = time.localtime(time.time())
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        self.writeToTxtAdd(file_path, str(current_time + ": " + content))

    def copyFile(self, fromfile=None, tofile=None):
        if fromfile is None or os.path.exists(fromfile) is False:
            print "Source file {0} is not exits".format(fromfile)
            return False
        try:
            retry = 1
            retryLimit = 60
            while not os.path.exists(tofile) and retry <= retryLimit:
                if retry > 1:
                    time.sleep(1)
                shutil.copy(fromfile, tofile)
                retry += 1
            if retryLimit < retry:
                raise Exception('Copy file retry limit time reached.')
            return True
        except Exception as e:
            raise Exception("Exception {0} to copy file {1} to file {2}.".format(e.message,
                                                                                 fromfile,
                                                                                 tofile))

    def updateData(self):
        while True:
            time.sleep(1)
            try:
                if os.path.exists(self.path):
                    fromFilePath = ''
                    message1 = "file: {0} exits and start to decompress.".format(self.path)
                    print message1
                    tar = tarfile.open(self.path, "r:gz")
                    file_names = tar.getnames()
                    data_length = len(file_names)
                    if data_length < 2:
                        print "no data to update."
                    for file_name in file_names:
                        fromFilePath = '/{0}'.format(file_name)
                        file_string_arrays = file_name.split('/')
                        currentFileName = file_string_arrays[len(file_string_arrays) - 1]
                        toFilePath = '{0}/{1}'.format(self.articlePath, currentFileName)
                        tar.extract(file_name, '/')
                        message2 = 'data {0} is decompressed done.'.format(currentFileName)
                        print message2
                        self.logger(self.logpath, message2)
                        retry = 1
                        retryLimit = 10
                        while not os.path.exists(toFilePath) and retry <= retryLimit:
                            if retry > 1:
                                time.sleep(1)
                            if self.copyFile(fromFilePath, toFilePath):
                                message3 = 'copy file: {0} done !'.format(currentFileName)
                                print message3
                                self.logger(self.logpath, message3)
                                os.remove(fromFilePath)
                                message4 = 'delete file: {0} done !'.format(currentFileName)
                                print message4
                                self.logger(self.logpath, message4)
                            retry += 1
                        if retry > retryLimit:
                            message5 = 'copyt file: {0} fail !'.format(currentFileName)
                            print message5
                            self.logger(self.logpath, message5)
                    message6 = 'decompress file: {0} done !'.format(self.path)
                    print message6
                    self.logger(self.logpath, message6)
                    tar.close()
                    os.remove(self.path)
                    message6 = 'delete file: {0} done !'.format(self.path)
                    print message6
                    self.logger(self.logpath, message6)
                    print "waiting..."
            except Exception as e:
                message3 = "Exception: {0} to update mongod: {1}.".format(e.message, fromFilePath)
                print message3
                self.logger(self.logpath, message3)

if __name__ == '__main__':
    u = UpdateHtml()
    u.updateData()