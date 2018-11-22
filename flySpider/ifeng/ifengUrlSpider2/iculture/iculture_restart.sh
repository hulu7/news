#!/bin/bash
MYDATE=$(date)
ps aux | grep "ifeng_iculture" |grep -v grep| cut -c 9-15 | xargs kill -9
runck=`ps -fe |grep "ifeng_iculture" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_iculture ..." >> /home/dev/Data/files/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/iculture/'
  python ifeng_iculture.py
else
  echo "${MYDATE}: ifeng_iculture spider is running" >> /home/dev/Data/files/ifeng/log/log.log
fi

