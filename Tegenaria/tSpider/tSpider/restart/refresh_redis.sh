#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
RPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/pholcus

sp=`ps -fe |grep "refresh_redis.py" |grep -v "grep" |wc -l`
if [ ${sp} -eq 0 ]; then
  echo "${TIME}: Refresh redis start shell ..." >> ${LOGPATH}/${DATE}_log.log
  python ${RPATH}/refresh_redis.py
else
  echo "${TIME}: Refresh redis is running" >> ${LOGPATH}/${DATE}_log.log
fi