DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
scriptDir=/home/dev/Data/dev
mode=dev
deploy=Repository
mongoDir=/home/${mode}/Data
echo "${TIME}: mongo master start"  >> ${scriptDir}/${DATE}_log.log
mongod --dbpath ${mongoDir}/mongodb/data