#!/bin/bash
MYDATE=$(date)
SENDPATH=/home/dev/Repository/news/supplier/send
isSendExists=`ps -fe |grep "send_data.py" |grep -v "grep" |wc -l`
if [ ${isSendExists} -eq 0 ]; then
   echo "${MYDATE}: Restart send ..."
   python ${SENDPATH}/send_data.py
else
   echo "${MYDATE}: send is running"
fi