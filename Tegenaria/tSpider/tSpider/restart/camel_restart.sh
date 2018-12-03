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

ce=`ps -fe |grep "ce_url.py" |grep -v "grep" |wc -l`
if [ ${ce} -eq 0 ]; then
  echo "${TIME}: Restart ce url spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/ce/ce_url.py
else
  echo "${TIME}: ce url is running" >> ${LOGPATH}/${DATE}_log.log
fi

yicai=`ps -fe |grep "yicai_url.py" |grep -v "grep" |wc -l`
if [ ${yicai} -eq 0 ]; then
  echo "${TIME}: Restart yicai url spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/yicai/yicai_url.py
else
  echo "${TIME}: yicai url is running" >> ${LOGPATH}/${DATE}_log.log
fi
