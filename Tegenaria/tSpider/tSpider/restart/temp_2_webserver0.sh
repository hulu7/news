#!/bin/bash
FILE_DATE=$(date "+%Y%m%d")
LOG_DATE=$(date "+%Y%m%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
FROMPATH=/home/dev/Data/Production/data4deepinews/html
TOPATH=/home/dev/Data/Production/article
LOGPATH=/home/dev/Data/rsyncData/prd4/log
for file in $(ls ${FROMPATH})
do
   echo "${TIME}: Start to upload html file ${file} ..." >> ${LOGPATH}/${LOG_DATE}_log.log
    expect -c "
      spawn scp ${FROMPATH}/${file} root@webserver0:${TOPATH}/
      expect {
        \"*assword\" {set timeout 60000; send \"rerr48779\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
      }
      expect eof"
    echo 'y' | rm ${FROMPATH}/${file}
    echo "${TIME}: Finish to upload html file ${file} and delete it." >> ${LOGPATH}/${LOG_DATE}_log.log
done