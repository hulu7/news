#!/bin/bash
FILE_DATE=$(date "+%Y-%m-%d")
LOG_DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
SALTICIDAEPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/talk
LOGPATH=/home/dev/Data/rsyncData/prd4/log
sm=`ps -fe |grep "weixin_talk.py" |grep -v "grep" |wc -l`
if [ $sm -eq 0 ]; then
     echo "${TIME}: Start to upload html and image files ..." >> ${LOGPATH}/${LOG_DATE}_log.log
     cd ${SALTICIDAEPATH}
     python weixin_talk.py
else
  echo "weixin_talk started"
fi