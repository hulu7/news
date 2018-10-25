#!/bin/bash
MYDATE=$(date)
ifashion=`ps -fe |grep "ifeng_ifashion" |grep -v "grep" |wc -l`
if [ $ifashion -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_ifashion ..." >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ifashion/'
  python ifeng_ifashion.py
else
  echo "${MYDATE}: ifeng_ifashion spider is running" >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
fi