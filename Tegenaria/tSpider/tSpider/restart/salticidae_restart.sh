#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SALTICIDAEPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/salticidae
for salticidae in $(ls ${SALTICIDAEPATH})
do
    if [ "${salticidae}" != "__init__.py" ]; then
        salticidaeExists=`ps -fe |grep "${salticidae}" |grep -v "grep" |wc -l`
        if [ ${salticidaeExists} -eq 0 ]; then
           echo "${TIME}: Restart ${salticidae} content salticidae ..." >> ${LOGPATH}/${DATE}_log.log
           python ${SALTICIDAEPATH}/${salticidae}
        else
           echo "${TIME}: ${salticidae} content is running" >> ${LOGPATH}/${DATE}_log.log
        fi
    fi
done
chmod 777 ${LOGPATH}/${DATE}_log.log