#!/bin/bash
MYDATE=$(date)
COMMITPATH=/home/dev/Repository/news/supplier/commit
isCommitExists=`ps -fe |grep "commit_data.py" |grep -v "grep" |wc -l`
if [ ${isCommitExists} -eq 0 ]; then
   echo "${MYDATE}: Restart commit ..."
   python ${COMMITPATH}/commit_data.py
else
   echo "${MYDATE}: commit is running"
fi