DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
scriptDir=/home/dev/Data/rsyncData/prd4/log
echo "${TIME}: shutdown system"  >> ${scriptDir}/${DATE}_log.log
ps aux | grep "mongoRestart_prd3.sh" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
ps aux | grep "python" |grep -v grep| cut -c 9-15 | xargs kill -9 >> ${scriptDir}/${DATE}_log.log
redis-cli -h 127.0.0.1 -p 6379 shutdown >> ${scriptDir}/${DATE}_log.log
service mongod stop  >> ${scriptDir}/${DATE}_log.log
shutdown >> ${scriptDir}/${DATE}_log.log