#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiders
for spider in $(ls ${SPIDERPATH})
do
    if [ "${spider}" != "__init__.py" ]; then
        spiderExists=`ps -fe |grep "${spider}" |grep -v "grep" |wc -l`
        if [ ${spiderExists} -eq 0 ]; then
           echo "${TIME}: Restart ${spider} content spider ..." >> ${LOGPATH}/${DATE}_log.log
           python ${SPIDERPATH}/${spider}
        else
           echo "${TIME}: ${spider} content is running" >> ${LOGPATH}/${DATE}_log.log
        fi
    fi
done
chmod 777 ${LOGPATH}/${DATE}_log.log