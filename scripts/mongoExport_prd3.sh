#!/bin/bash
tmpDir=/home/Data
prd3Path=/home/dev/Data/rsyncData/prd3
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=/home/dev/Data/rsyncData/prd3/log
CAMELPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel
for camel in $(ls ${CAMELPATH})
do
    if [ "${camel}" != "__init__.py" ]; then
        domain_name=${camel%_*}
        syncDir=${prd3Path}/${domain_name}
        echo "${TIME}: Start to exprot ${domain_name}..." >> ${LOGPATH}/${DATE}_log.log
        mongoexport -d ${domain_name}_urls -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/${domain_name}_urls_tmp.csv
        mv ${tmpDir}/${domain_name}_urls_tmp.csv ${syncDir}/${domain_name}_urls.csv
        chmod 777 ${syncDir}/${domain_name}_urls.csv
    fi
done