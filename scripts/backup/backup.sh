#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
logDir=/home/dev/Data/rsyncData/backuplog
echo "${TIME}: backup start"
echo "${TIME}: backup start"  >> ${logDir}/${DATE}_log.log
if [ -n "$1" ] && [ -n "$2" ]; then
    fromPath=$1
    toPath=$2
    echo "${TIME}: from path: $fromPath, to path: $toPath"
    echo "${TIME}: from path: $fromPath, to path: $toPath"  >> ${logDir}/${DATE}_log.log
    expect -c "
      spawn scp -r ${fromPath} root@prd5:${toPath}
      expect {
        \"*assword\" {set timeout 600; send \"thebestornothing\r\";}
        \"yes/no\" {send \"yes\r\"; exp_continue;}
      }
      expect eof"
else
    echo "${TIME}: error"
    echo "${TIME}: error"  >> ${logDir}/${DATE}_log.log
fi
