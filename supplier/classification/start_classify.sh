#!/bin/bash
MYDATE=$(date)
CLASSIFYPATH=/home/dev/Repository/news/supplier/classification
isClassifyExists=`ps -fe |grep "start_classify.py" |grep -v "grep" |wc -l`
if [ ${isClassifyExists} -eq 0 ]; then
   echo "${MYDATE}: Restart classify ..."
   python ${CLASSIFYPATH}/start_classify.py
else
   echo "${MYDATE}: classify is running"
fi