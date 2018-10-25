#!/bin/bash
MYDATE=$(date)
echo "${MYDATE}: restarting global_restart ..." >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
echo "${MYDATE}: starting spiders ..." >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ihistory/'
sh ihistory_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/imil/'
sh imil_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/inews/'
sh inews_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ient/'
sh ient_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ifashion/'
sh ifashion_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ifinance/'
sh ifinance_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/isports/'
sh isports_restart.sh
cd '/home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/itech/'
sh itech_restart.sh
ps aux | grep "global_restart" |grep -v grep| cut -c 9-15 | xargs kill -9
echo "${MYDATE}: restarted global_restart ..." >> /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/log.log