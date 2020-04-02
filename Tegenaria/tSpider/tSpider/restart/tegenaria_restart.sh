#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SPIDERPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/spiders
echo "${TIME}: Restart content spider ..." >> ${LOGPATH}/${DATE}_log.log
python ${SPIDERPATH}/spider_run.py