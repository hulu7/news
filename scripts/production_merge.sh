DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/rsyncData/prd4/log
SCRIPTS=/home/dev/Repository/news/scripts
echo "${TIME}: merge production start" >> ${LOG}/${DATE}_log.log
python ${SCRIPTS}/production_merge.py