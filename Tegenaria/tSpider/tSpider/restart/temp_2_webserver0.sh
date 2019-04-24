#!/bin/bash
FILE_DATE=$(date "+%Y%m%d")
LOG_DATE=$(date "+%Y%m%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
FROMROOTPATH=/home/dev/Data/Production/data4deepinews
TOROOTPATH=/home/dev/Data/Production
FROMHTMLPATH=${FROMROOTPATH}/html
FROMIMGPATH=${FROMROOTPATH}/img
TOHTMLPATH=${TOROOTPATH}/article
TOIMGPATH=${TOROOTPATH}/img
LOGPATH=/home/dev/Data/rsyncData/prd4/log
for file in $(ls ${FROMHTMLPATH})
do
   echo "${TIME}: Start to upload html file ${file} ..." >> ${LOGPATH}/${LOG_DATE}_log.log
    expect -c "
      spawn scp ${FROMHTMLPATH}/${file} root@webserver0:${TOHTMLPATH}/
      expect {
        \"*assword\" {set timeout 60000; send \"rerr48779\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
      }
      expect eof"
    echo 'y' | rm ${FROMHTMLPATH}/${file}
    echo "${TIME}: Finish to upload html file ${file} and delete it." >> ${LOGPATH}/${LOG_DATE}_log.log
done
for file in $(ls ${FROMIMGPATH})
do
   echo "${TIME}: Start to upload image file ${file} ..." >> ${LOGPATH}/${LOG_DATE}_log.log
    expect -c "
      spawn scp ${FROMIMGPATH}/${file} root@webserver0:${TOIMGPATH}/
      expect {
        \"*assword\" {set timeout 60000; send \"rerr48779\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
      }
      expect eof"
    echo 'y' | rm ${FROMIMGPATH}/${file}
    echo "${TIME}: Finish to upload html file ${file} and delete it." >> ${LOGPATH}/${LOG_DATE}_log.log
done