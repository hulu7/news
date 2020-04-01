#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiderMonitor
isSpiderRun=`ps -fe |grep "monitorRun.py" |grep -v "grep" |wc -l`
if [ ${isSpiderRun} -eq 0 ]; then
   echo "${TIME}: Restart monitor ..." >> ${LOGPATH}/${DATE}_log.log
   python ${SPIDERPATH}/monitorRun.py
else
   echo "${TIME}: ssh monitor is running" >> ${LOGPATH}/${DATE}_log.log
fi