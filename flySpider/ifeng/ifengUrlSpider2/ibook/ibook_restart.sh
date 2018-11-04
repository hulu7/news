#!/bin/bash
MYDATE=$(date)
ps aux | grep "ifeng_ibook" |grep -v grep| cut -c 9-15 | xargs kill -9
runck=`ps -fe |grep "ifeng_ibook" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_ibook ..." >> /home/dev/Repository_Test_Data/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ibook/'
  python ifeng_ibook.py
else
  echo "${MYDATE}: ifeng_ibook spider is running" >> /home/dev/Repository_Test_Data/ifeng/log/log.log
fi
