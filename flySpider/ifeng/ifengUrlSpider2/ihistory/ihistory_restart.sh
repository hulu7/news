#!/bin/bash
MYDATE=$(date)
runck=`ps -fe |grep "ifeng_ihistory" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_ihistory ..." >> /home/dev/Data/files/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ihistory/'
  python ifeng_ihistory.py
else
  echo "${MYDATE}: ifeng_ihistory spider is running" >> /home/dev/Data/files/ifeng/log/log.log
fi

