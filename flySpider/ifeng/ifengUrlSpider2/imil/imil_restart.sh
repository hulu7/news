#!/bin/bash
MYDATE=$(date)
runck=`ps -fe |grep "ifeng_imil" |grep -v "grep" |wc -l`
if [ $runck -eq 0 ]; then
  echo "${MYDATE}: starting ifeng_imil ..." >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
  cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/imil/'
  python ifeng_imil.py
else
  echo "${MYDATE}: ifeng_imil spider is running" >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
fi

