#!/bin/bash
MYDATE=$(date)
runck=`ps -fe |grep "ifeng_isports" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_isports ..." >> /home/dev/Data/files/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/isports/'
  python ifeng_isports.py
else
  echo "${MYDATE}: ifeng_isports spider is running" >> /home/dev/Data/files/ifeng/log/log.log
fi

