DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
scriptDir=/home/dev/Data/rsyncData/prd4/log
mode=dev
deploy=Repository
mongoDir=/home/${mode}/Data
echo "${TIME}: mongo master start"  >> ${scriptDir}/${DATE}_log.log
mongod --repair --dbpath ${mongoDir}/mongodb/data