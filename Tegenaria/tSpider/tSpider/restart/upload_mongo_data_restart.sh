#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SCRIPTPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/uploadMongoData
isScriptRun=`ps -fe |grep "uploadMongoData.py" |grep -v "grep" |wc -l`
if [ ${isScriptRun} -eq 0 ]; then
   echo "${TIME}: Restart upload mongo data ..." >> ${LOGPATH}/${DATE}_log.log
   python ${SCRIPTPATH}/uploadMongoData.py
else
   echo "${TIME}: upload mongo data is running" >> ${LOGPATH}/${DATE}_log.log
fi