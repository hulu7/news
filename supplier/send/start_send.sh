#!/bin/bash
MYDATE=$(date)
cd '/home/dev/Repository/news/supplier/send/'
echo "${MYDATE}: start send ..."
python send_data.py
echo "${MYDATE}: end send"