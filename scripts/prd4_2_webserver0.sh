#!/bin/bash
FILE_DATE=$(date "+%Y-%m-%d")
LOG_DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
OUTPATH=/home/dev/Data/Production/data4deepinews
LOGPATH=/home/dev/Data/rsyncData/prd4/log
SERVERINFO=/home/dev/Repository/news/servers/webserver0.txt
ip=''
password=''
while read line
do
    echo $line
    info=(${line//==/ })
    ip=${info[0]}
    password=${info[1]}
done < ${SERVERINFO}
echo ${ip}
echo ${password}
isWorking=`ps -fe |grep "update_mongo_deepnews.py" |grep -v "grep" |wc -l`
if [ ${isWorking} -eq 0 ]; then
   echo "${TIME}: Start to update DeepINews ..." >> ${LOGPATH}/${LOG_DATE}_log.log
    expect -c "
      spawn scp ${OUTPATH}/${FILE_DATE}.csv root@${ip}:${OUTPATH}/
      expect {
        \"*assword\" {set timeout 60000; send \"${password}\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
      }
      expect eof"
    echo 'y' | rm ${OUTPATH}/${FILE_DATE}.csv
else
   echo "${TIME}: ${USER} is running" >> ${LOGPATH}/${LOG_DATE}_log.log
fi