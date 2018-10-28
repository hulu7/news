#!/bin/bash
MYDATE=$(date)
echo "${MYDATE}: restarting global_restart ..." >> /home/dev/Repository_Test_Data/ifeng/log/log.log
echo "${MYDATE}: starting spiders ..." >> /home/dev/Repository_Test_Data/ifeng/log/log.log
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ihistory/ihistory_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/imil/imil_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/inews/inews_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ient/ient_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ifashion/ifashion_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ifinance/ifinance_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/isports/isports_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/itech/itech_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/iculture/iculture_restart.sh
sh /home/dev/Repository/news/flySpider/ifeng/ifengUrlSpider2/ibook/ibook_restart.sh
ps aux | grep "global_restart" |grep -v grep| cut -c 9-15 | xargs kill -9
echo "${MYDATE}: restarted global_restart ..." >> /home/dev/Repository_Test_Data/ifeng/log/log.log