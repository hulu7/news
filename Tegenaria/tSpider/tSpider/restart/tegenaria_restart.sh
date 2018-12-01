#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiders

huxiu=`ps -fe |grep "huxiu.py" |grep -v "grep" |wc -l`
if [ ${huxiu} -eq 0 ]; then
  echo "${TIME}: Restart huxiu content spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/huxiu.py
else
  echo "${TIME}: huxiu content is running" >> ${LOGPATH}/${DATE}_log.log
fi

ifeng=`ps -fe |grep "ifeng.py" |grep -v "grep" |wc -l`
if [ ${ifeng} -eq 0 ]; then
  echo "${TIME}: Restart ifeng content spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/ifeng.py
else
  echo "${TIME}: ifeng content is running" >> ${LOGPATH}/${DATE}_log.log
fi
chmod 777 ${LOGPATH}/${DATE}_log.log