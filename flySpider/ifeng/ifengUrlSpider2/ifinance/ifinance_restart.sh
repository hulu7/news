#!/bin/bash
MYDATE=$(date)
runck=`ps -fe |grep "ifeng_ifinance" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_ifinance ..." >> /home/dev/Data/files/ifeng/log/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ifinance/'
  python ifeng_ifinance.py
else
  echo "${MYDATE}: ifeng_ifinance spider is running" >> /home/dev/Data/files/ifeng/log/log.log
fi

