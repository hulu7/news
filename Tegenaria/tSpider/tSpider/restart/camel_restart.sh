#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
CAMELPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel
echo "${TIME}: Restart url spider ..." >> ${LOGPATH}/${DATE}_log.log
python ${CAMELPATH}/camel_run.py