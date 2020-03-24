#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/storeHtml
isSpiderRun=`ps -fe |grep "sshUpload.py" |grep -v "grep" |wc -l`
if [ ${isSpiderRun} -eq 0 ]; then
   echo "${TIME}: Restart ssh upload ..." >> ${LOGPATH}/${DATE}_log.log
   python ${SPIDERPATH}/sshUpload.py
else
   echo "${TIME}: ssh upload running" >> ${LOGPATH}/${DATE}_log.log
fi