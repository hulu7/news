DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
logPath=/home/dev/Data/rsyncData/prd4/log
mode=dev
deploy=Repository
mongoDir=/home/${mode}/Data
echo "${TIME}: mongo master start"  >> ${logPath}/${DATE}_log.log
mongod --dbpath ${mongoDir}/mongodb/data