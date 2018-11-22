MYDATE=$(date)
scriptDir=/home/dev/Data/rsyncData/prd1
echo "${MYDATE}: Spider deploy start"  >> ${scriptDir}/log.txt
mode=dev
deploy=Repository
redisDir=/usr/local/bin/
mongoDir=/home/${mode}/Data
spiderDir=/home/${mode}/${deploy}/news/flySpider/ifeng/ifengSpider/
echo "${MYDATE}: start redis server"  >> ${scriptDir}/log.txt
cd ${redisDir}
./redis-server
echo "${MYDATE}: start scrapy server" >> ${scriptDir}/log.txt
cd ${spiderDir}
scrapyd
echo "${MYDATE}: deploy ifeng" >> ${scriptDir}/log.txt
cd ${spiderDir}
python scrapyd-deploy 4 -p ifeng --version v1
echo "${MYDATE}: mongo master start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb/data --replSet repset
echo "${MYDATE}: mongo slave1 start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb_slave1/data --port 27018 --replSet repset
echo "${MYDATE}: mongo slave2 start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb_slave2/data --port 27019 --replSet repset
echo "${MYDATE}: mongo config" >> ${scriptDir}/log.txt
mongo
echo "config = config = {_id:"repset", members:[{_id:0, host:"127.0.0.1:27017"}, {_id:1, host:"127.0.0.1:27018"}, {_id:2, host:"127.0.0.1:27019"}]}"
echo "rs.initiate(config)"
echo "${MYDATE}: start crawl"  >> ${scriptDir}/log.txt
ifeng=`ps -fe |grep "scrapy crawl ifeng" |grep -v "grep" |wc -l`
if [ $ifeng -eq 0 ]; then
    echo "starting ifeng..." >> ${scriptDir}/log.txt
    cd ${spiderDir}
    scrapy crawl ifeng
else
  echo "ifeng started" >> ${scriptDir}/log.txt
fi