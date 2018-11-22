#!/bin/bash
MYDATE=$(date)
cd '/home/dev/Repository/news/supplier/commit/'
echo "${MYDATE}: start commit ..."
python commit_data.py
chmod -R 777 /home/dev/Data/Production
echo "${MYDATE}: end commit"