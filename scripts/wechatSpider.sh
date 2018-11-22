#!/bin/bash
MYDATE=$(date)
cd '/home/dev/Repository/news/scripts/'
echo "${MYDATE}: start wechatSpider ..."
python wechatSpider.py
chmod -R 777 /home/dev/Data/Production
echo "${MYDATE}: end wechatSpider"