import subprocess
import os
# processes=subprocess.Popen('start powershell.exe', shell=True)
os.system("cd "C:\\Program Files\\Redis"")
os.system(".\redis-server")
os.system("cd "C:\\Program Files\\Redis"")
os.system(".\redis-cli")
os.system("mongod --dbpath D:\\flySpider\\db\\master\\data --replSet repset")
os.system("mongod --dbpath D:\\flySpider\\db\\slave_1\\data --port 27018 --replSet repset")
os.system("mongod --dbpath D:\\flySpider\\db\\slave_2\\data --port 27019 --replSet repset")
os.system("mongo")
os.system("use admin")
os.system("
  config={ _id: "repset", members:[
    {_id:0, host: "127.0.0.1:27017"},
    {_id:1, host: "127.0.0.1:27018"},
    {_id:2, host: "127.0.0.1:27019"}]
    }
")
os.system("
rs.initiate(config)
")
os.system("cd D:\\flySpider\\huxiu\\huSpider")
os.system("scrapyd")
os.system("cd D:\\flySpider\\huxiu\\huSpider")
os.system("python scrapyd-deploy 50 -p huxiu --version v1")
os.system("cd D:\\flySpider\\huxiu\\huSpider")
os.system("scrapy crawl huxiu")

# 也就是意外推出时数据被锁定了，登陆mongo给的推荐链接找到了解决办法：
#   1.删除锁文件，这个锁文件位于你存储data数据的目录
# rm D:\\flySpider\\db\\master\\data\\mongod.lock
#    2.修复数据文件
# mongod --dbpath D:\\flySpider\\db\\master\\data --repair
#  3.重启mongo
# mongod --dbpath D:\\flySpider\\db\\master\\data
# 好了，启动成功。