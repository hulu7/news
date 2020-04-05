DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
SCRIPTS=/home/dev/Repository/news/scripts
echo "${TIME}: start to update deepinews"  >> ${LOG}/${DATE}_log.log
sp=`ps -fe |grep "update_mongo_deepinews.py" |grep -v "grep" |wc -l`
if [ ${sp} -eq 0 ]; then
  echo "${TIME}: Update mongo data start..." >> ${LOG}/${DATE}_log.log
  python ${SCRIPTS}/update_mongo_deepinews.py >> ${LOG}/${DATE}_log.log
else
  echo "${TIME}: Update mongo data is running" >> ${LOG}/${DATE}_log.log
fi
