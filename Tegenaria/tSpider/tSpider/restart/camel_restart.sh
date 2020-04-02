#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
CAMELPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel
isCamelRun=`ps -fe |grep "camel_run.py" |grep -v "grep" |wc -l`
if [ ${isCamelRun} -eq 0 ]; then
   echo "${TIME}: Restart url spider ..." >> ${LOGPATH}/${DATE}_log.log
   python ${CAMELPATH}/camel_run.py
else
   echo "${TIME}: camel is running" >> ${LOGPATH}/${DATE}_log.log
fi