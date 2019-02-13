DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
SCRIPTS=/home/dev/Repository/news/scripts
echo "${TIME}: start to update deepinews"  >> ${LOG}/${DATE}_log.log
python ${SCRIPTS}/update_mongo_deepinews.py >> ${LOG}/${DATE}_log.log
