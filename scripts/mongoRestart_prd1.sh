MYDATE=$(date)
scriptDir=/home/dev/Data/rsyncData/prd1
echo "${MYDATE}: Spider deploy start"  >> ${scriptDir}/log.txt
mode=dev
deploy=Repository
redisDir=/usr/local/bin/
mongoDir=/home/${mode}/Data
echo "${MYDATE}: start redis server"  >> ${scriptDir}/log.txt
cd ${redisDir}
./redis-server
echo "${MYDATE}: mongo master start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb/data --replSet repset
echo "${MYDATE}: mongo slave1 start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb_slave1/data --port 27018 --replSet repset
echo "${MYDATE}: mongo slave2 start"  >> ${scriptDir}/log.txt
mongod --dbpath ${mongoDir}/mongodb_slave2/data --port 27019 --replSet repset
echo "${MYDATE}: mongo config"  >> ${scriptDir}/log.txt
mongo
echo "config = config = {_id:"repset", members:[{_id:0, host:"127.0.0.1:27017"}, {_id:1, host:"127.0.0.1:27018"}, {_id:2, host:"127.0.0.1:27019"}]}"
echo "rs.initiate(config)"

