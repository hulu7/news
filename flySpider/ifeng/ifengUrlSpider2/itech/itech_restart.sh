#!/bin/bash
MYDATE=$(date)
runck=`ps -fe |grep "itech_ifinance" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_itech ..." >> /home/dev/Repository_Test_Data/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/itech/'
  python ifeng_itech.py
else
  echo "${MYDATE}: ifeng_itech spider is running" >> /home/dev/Repository_Test_Data/ifeng/log/log.log
fi
