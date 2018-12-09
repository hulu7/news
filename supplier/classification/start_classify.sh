#!/bin/bash
MYDATE=$(date)
cd '/home/dev/Repository/news/supplier/classification/'
echo "${MYDATE}: start classify ..."
python start_classify.py
chmod -R 777 /home/dev/Data/Production
echo "${MYDATE}: end classify"