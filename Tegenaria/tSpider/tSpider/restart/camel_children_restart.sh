#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
CAMELPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel_children_url
for camel in $(ls ${CAMELPATH})
do
    if [ "${camel}" != "__init__.py" ] && [ "${camel}" != "sp_url.py" ]; then
        camelExists=`ps -fe |grep "${camel}" |grep -v "grep" |wc -l`
        if [ ${camelExists} -eq 0 ]; then
           echo "${TIME}: Restart ${camel} content spider ..." >> ${LOGPATH}/${DATE}_log.log
           python ${CAMELPATH}/${camel}
        else
           echo "${TIME}: ${camel} content is running" >> ${LOGPATH}/${DATE}_log.log
        fi
    fi
done