# -*- coding: utf-8 -*-
import os
import oss2

class AliUpload():
    def __init__(self, fileDirectory=None,
                       fileName=None,
                       bucketName=None,
                       bucketFolderName=None):
        self.fileDirectory = fileDirectory
        self.fileName = fileName
        self.bucketName = bucketName
        self.bucketFolderName = bucketFolderName
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('LTAI4FnW1WfPEP3KS9Wp7sj2', '2wniMzTK2gpQCYDKanvZkQyLOnHrIz')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '{0}'.format(self.bucketName))

    def start(self):
        try:
            # 必须以二进制的方式打开文件，因为需要知道文件包含的字节数。
            with open('{0}/{1}'.format(self.fileDirectory, self.fileName), 'rb') as fileobj:
                result = self.bucket.put_object('{0}/{1}'.format(self.bucketFolderName, self.fileName), fileobj)
                if result.status == 200:
                    print 'Upload file {0} success!'.format(self.fileName)
                    return True
                return False
        except Exception as e:
            print 'Exception {0} to upload files: {1}'.format(e.message, self.fileName)
            return False

