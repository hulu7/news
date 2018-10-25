#!/bin/bash
MYDATE=$(date)
runck=`ps -fe |grep "ifeng_inews" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_inews ..." >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/inews/'
  python ifeng_inews.py
else
  echo "${MYDATE}: ifeng_inews spider is running" >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
fi

