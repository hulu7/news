# -*- coding:utf-8 -*-
import paramiko

class SSHUpload():
    def start(self, address, port, username, password, fromFile, toFile):
        transport = paramiko.Transport((address, port))
        try:
            print 'Start to upload file: {0}'.format(fromFile)
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(fromFile, toFile)
            transport.close()
            print 'Finished to upload file: {0}'.format(fromFile)
            return True
        except Exception as e:
            print 'Exception {0} to upload file: {1}'.format(e.message, fromFile)
            return False