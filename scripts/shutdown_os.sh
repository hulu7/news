DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
scriptDir=/home/dev/Data/rsyncData/prd4/log
echo "${TIME}: shutdown system"
echo "${TIME}: shutdown system"  >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: kill camel_restart"
ps aux | grep "camel_restart" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: kill tegenaria_restart"
ps aux | grep "tegenaria_restart" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: kill python"
ps aux | grep "python" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: kill mongoRestart"
ps aux | grep "mongoRestart" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: kill redis_restart"
ps aux | grep "redis_restart" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: stop redis"
redis-cli -h 127.0.0.1 -p 6379 shutdown >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: stop mongodb"
service mongod stop >> ${scriptDir}/${DATE}_log.log
echo 'y' | rm /home/dev/Data/mongodb/data/mongod.lock >> ${scriptDir}/${DATE}_log.log
echo "${TIME}: rm dump.rdb"
cd ~
echo 'y' | rm dump.rdb >> ${scriptDir}/${DATE}_log.log
shutdown >> ${scriptDir}/${DATE}_log.log