#!/bin/bash
MYDATE=$(date)
cd '/home/dev/Repository/news/supplier/classification/'
echo "${MYDATE}: start ifeng classify ..."
python ifeng_class.py
chmod -R 777 /home/dev/Data/Production
echo "${MYDATE}: end ifeng classify"