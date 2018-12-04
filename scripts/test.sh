#!/bin/bash
MYDATE=$(date "+%Y-%m-%d")
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel
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