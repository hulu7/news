#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel

huxiu=`ps -fe |grep "huxiu_url.py" |grep -v "grep" |wc -l`
if [ ${huxiu} -eq 0 ]; then
  echo "${TIME}: Restart huxiu url spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/huxiu/huxiu_url.py
else
  echo "${TIME}: huxiu url is running" >> ${LOGPATH}/${DATE}_log.log
fi
