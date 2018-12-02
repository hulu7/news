#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel

sp=`ps -fe |grep "sp_url.py" |grep -v "grep" |wc -l`
if [ ${sp} -eq 0 ]; then
  echo "${TIME}: Restart sp url spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/sp/sp_url.py
else
  echo "${TIME}: sp url is running" >> ${LOGPATH}/${DATE}_log.log
fi
