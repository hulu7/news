# -*- coding:utf-8 -*-
import paramiko

transport = paramiko.Transport(('223.111.139.227', 22))
transport.connect(username='root', password='rerr48779')

sftp = paramiko.SFTPClient.from_transport(transport)

sftp.put('/home/dev/Repository/news/scripts/template.html', '/home/dev/template.html')

transport.close()

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('223.111.139.227', 22, 'root', 'rerr48779')
#
# sftp = ssh.open_sftp()
# sftp.put('/home/dev/Repository/news/scripts/template.html', '/home/dev/template.html')