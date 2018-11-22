MYDATE=$(date)
scriptDir=/home/dev/Data/Production/log
mode=dev
deploy=Repository
mongoDir=/home/${mode}/Data
echo "${MYDATE}: mongo master start"  >> ${scriptDir}/log.log
mongod --dbpath ${mongoDir}/mongodb/data --replSet repset
echo "${MYDATE}: mongo slave1 start"  >> ${scriptDir}/log.log
mongod --dbpath ${mongoDir}/mongodb_slave1/data --port 27018 --replSet repset
echo "${MYDATE}: mongo slave2 start"  >> ${scriptDir}/log.log
mongod --dbpath ${mongoDir}/mongodb_slave2/data --port 27019 --replSet repset
echo "${MYDATE}: mongo config" >> ${scriptDir}/log.log
mongo
echo "config = config = {_id:"repset", members:[{_id:0, host:"127.0.0.1:27017"}, {_id:1, host:"127.0.0.1:27018"}, {_id:2, host:"127.0.0.1:27019"}]}"
echo "rs.initiate(config)"