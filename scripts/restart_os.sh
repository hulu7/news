DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
scriptDir=/home/dev/Data/rsyncData/prd4/log
echo "${TIME}: shutdown system"  >> ${scriptDir}/${DATE}_log.log
redis-cli -h 127.0.0.1 -p 6379 shutdown >> ${scriptDir}/${DATE}_log.log
service mongod stop >> ${scriptDir}/${DATE}_log.log
reboot >> ${scriptDir}/${DATE}_log.log