#!/bin/bash
tmpDir=/home/Data
prd4Path=/home/dev/Data/rsyncData/prd4
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=${prd4Path}/log
CAMELPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/camel
for camel in $(ls ${CAMELPATH})
do
    if [ "${camel}" != "__init__.py" ]; then
        domain_name=${camel%_*}
        syncDir=${prd4Path}/${domain_name}
        echo "${TIME}: Start to exprot ${domain_name}..." >> ${LOGPATH}/${DATE}_log.log
        mongoexport -d ${domain_name} -c 'contentInfo' --csv -f id,title,url,author_name,time,download_time,is_open_cache,source -q "{'download_time': '${DATE}'}" -o ${tmpDir}/${domain_name}_content_tmp.csv
        mv ${tmpDir}/${domain_name}_content_tmp.csv ${syncDir}/${domain_name}_content.csv
        chmod 777 ${syncDir}/${domain_name}_content.csv
    fi
done