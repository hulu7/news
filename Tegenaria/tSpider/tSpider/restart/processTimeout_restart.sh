#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
SRCPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/timeoutHandle

sp=`ps -fe |grep "timeoutHandler.py" |grep -v "grep" |wc -l`
if [ ${sp} -eq 0 ]; then
  echo "${TIME}: Restart timeout process ..."
  echo "${TIME}: Restart timeout process ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SRCPATH}/timeoutHandler.py
else
  echo "${TIME}: Timeout process is running"
  echo "${TIME}: Timeout process is running" >> ${LOGPATH}/${DATE}_log.log
fi