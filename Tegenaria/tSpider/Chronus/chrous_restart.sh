#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
CHRONUSPATH=/home/dev/Repository/news/Tegenaria/tSpider/Chronus
isChronusExists=`ps -fe |grep "chronus.py" |grep -v "grep" |wc -l`
if [ ${isChronusExists} -eq 0 ]; then
   echo "${TIME}: Restart chronus ..." >> ${LOGPATH}/${DATE}_log.log
   python ${CHRONUSPATH}/chronus.py
else
   echo "${TIME}: chronus is running" >> ${LOGPATH}/${DATE}_log.log
fi