MYDATE=$(date)
scriptDir=`cd $(dirname $0); pwd -P`
echo "${MYDATE}: Spider deploy start"  >> ${scriptDir}/log.txt
mode=dev
deploy=Repository
redisDir=/usr/local/bin/
mongoDir=/home/${mode}/Data
spiderDir=/home/${mode}/${deploy}/news/flySpider/ifeng/ifengSpider/
echo "${MYDATE}: start redis server"  >> ${scriptDir}/log.txt
cd ${redisDir}
./redis-server
echo "${MYDATE}: start scrapy server"  >> ${scriptDir}/log.txt
cd ${spiderDir}
scrapyd
echo "${MYDATE}: deploy ifeng"  >> ${scriptDir}/log.txt
cd ${spiderDir}
python scrapyd-deploy 3 -p ifeng --version v${MYDATE}
echo "${MYDATE}: start crawl"  >> ${scriptDir}/log.txt
cd ${spiderDir}
scrapy crawl ifeng
echo "${MYDATE}: mongo master start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb/data --replSet repset
echo "${MYDATE}: mongo slave1 start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb_slave1/data --port 27018 --replSet repset
echo "${MYDATE}: mongo slave2 start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb_slave2/data --port 27019 --replSet repset