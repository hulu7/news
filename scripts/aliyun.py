# -*- coding: utf-8 -*-
import os
import oss2

# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth('LTAI4FnW1WfPEP3KS9Wp7sj2', '2wniMzTK2gpQCYDKanvZkQyLOnHrIz')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'deepinews')

# 必须以二进制的方式打开文件，因为需要知道文件包含的字节数。
with open('/home/dev/Repository/news/Tegenaria/tSpider/tSpider/storeHtml/20c01fe6dd521b22291f649f7afc4437_4.jpg', 'rb') as fileobj:
    # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
    # fileobj.seek(1000, os.SEEK_SET)
    # Tell方法用于返回当前位置。
    # current = fileobj.tell()
    result = bucket.put_object('img/20c01fe6dd521b22291f649f7afc4437_4.jpg', fileobj)
    if result.status == 200:
        print 'Upload success!'