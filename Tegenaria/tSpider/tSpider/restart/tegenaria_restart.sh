#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiders
isSpiderRun=`ps -fe |grep "spider_run.py" |grep -v "grep" |wc -l`
if [ ${isSpiderRun} -eq 0 ]; then
   echo "${TIME}: Restart content spider ..." >> ${LOGPATH}/${DATE}_log.log
   python ${SPIDERPATH}/spider_run.py
else
   echo "${TIME}: spider is running" >> ${LOGPATH}/${DATE}_log.log
fi
chmod 777 ${LOGPATH}/${DATE}_log.log