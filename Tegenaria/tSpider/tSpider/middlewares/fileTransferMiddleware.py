#coding:utf-8
#------requirement------
#paramiko-2.4.2
#pyOpenSSL-0.13.1
#cryptography-1.7.2
#------requirement------
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import gc
import paramiko
import logging
from multiprocessing.pool import ThreadPool as Pool
sys.path.append("/home/dev/Repository/news/Tegenaria/tSpider/tSpider/")
from settings import Settings

class FileTransferMiddleware():
    def __init__(self):
        self.settings = Settings()
        self.settings.CreateCommonSettings()
        logging.raiseExceptions = False

    def singleUpload(self, local_file_path, remote_file_path, host_name, user_name, password, port):
        connect_port = paramiko.Transport((host_name, port))
        connect_port.connect(username=user_name, password=password)
        sftp = paramiko.SFTPClient.from_transport(connect_port)
        try:
            print 'start to transfer: {0}'.format(local_file_path)
            sftp.put(local_file_path, remote_file_path)
            connect_port.close()
            print 'finished to transfer: {0}'.format(local_file_path)
            print 'start to delete: {0}'.format(local_file_path)
            os.remove(local_file_path)
            print 'finished to delete: {0}'.format(local_file_path)
        except Exception as e:
            print 'Exception to transfer: {0} for {1}'.format(local_file_path, e.message)
        del connect_port, sftp
        gc.collect()

    def startUpload(self, local_diractory, remote_diractory, processes, host_name, user_name, password, port):
        isLocalDiractoryExists = os.path.exists(local_diractory)
        if isLocalDiractoryExists is False:
            print '{0} is not exits'.format(local_diractory)
            return
        files = os.listdir(local_diractory)
        if len(files) == 0:
            print 'No new file to upload in {0}'.format(local_diractory)
            return
        process = Pool(processes)
        for file in files:
            local_file_path = '{0}/{1}'.format(local_diractory, file)
            remote_file_path = '{0}/{1}'.format(remote_diractory, file)
            process.apply_async(self.singleUpload, args=(local_file_path,
                                                         remote_file_path,
                                                         host_name,
                                                         user_name,
                                                         password,
                                                         port))
        process.close()
        process.join()
        print 'Done'
        del files, process
        gc.collect()



