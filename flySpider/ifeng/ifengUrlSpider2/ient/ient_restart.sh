#!/bin/bash
MYDATE=$(date)
ps aux | grep "ifeng_ient" |grep -v grep| cut -c 9-15 | xargs kill -9
ient=`ps -fe |grep "ifeng_ient" |grep -v "grep" |wc -l`
if [ $ient -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_ient ..." >> /home/dev/Data/files/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ient/'
  python ifeng_ient.py
else
  echo "${MYDATE}: ifeng_ient spider is running" >> /home/dev/Data/files/ifeng/log/log.log
fi