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

ce=`ps -fe |grep "ce.py" |grep -v "grep" |wc -l`
if [ ${ce} -eq 0 ]; then
  echo "${TIME}: Restart ce content spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/ce.py
else
  echo "${TIME}: ce content is running" >> ${LOGPATH}/${DATE}_log.log
fi

yicai=`ps -fe |grep "yicai.py" |grep -v "grep" |wc -l`
if [ ${yicai} -eq 0 ]; then
  echo "${TIME}: Restart yicai content spider ..." >> ${LOGPATH}/${DATE}_log.log
  python ${SPIDERPATH}/yicai.py
else
  echo "${TIME}: yicai content is running" >> ${LOGPATH}/${DATE}_log.log
fi

chmod 777 ${LOGPATH}/${DATE}_log.log