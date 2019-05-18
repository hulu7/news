#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiders_huxiu
spiderExists=`ps -fe |grep "huxiu_nlp.py" |grep -v "grep" |wc -l`
if [ ${spiderExists} -eq 0 ]; then
   echo "${TIME}: Restart huxiu_nlp.py content spider ..." >> ${LOGPATH}/${DATE}_log.log
   python ${SPIDERPATH}/huxiu_nlp.py
else
   echo "${TIME}: huxiu_nlp.py content is running" >> ${LOGPATH}/${DATE}_log.log
fi