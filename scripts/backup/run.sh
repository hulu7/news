#!/bin/bash
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
logDir=/home/dev/Data/rsyncData/backuplog
scriptDir=/home/dev/Repository/news/scripts/backup
echo "${TIME}: read files"
echo "${TIME}: read files"  >> ${logDir}/${DATE}_log.log
if [ -n "$1" ]; then
    file=$1
    echo "${TIME}: start to read file $file"  >> ${logDir}/${DATE}_log.log
    for line in $(cat $file)
        do
            echo $line
            echo $line >> ${logDir}/${DATE}_log.log
            array=(${line//:/ })
            fromPath=${array[0]}
            toPath=${array[1]}
            ${scriptDir}/backup.sh ${fromPath} ${toPath}
    done
else
    echo "${TIME}: error"
    echo "${TIME}: error"  >> ${logDir}/${DATE}_log.log
fi
