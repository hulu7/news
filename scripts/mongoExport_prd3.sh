#!/bin/bash
tmpDir=/home/dev/Data
prd3Path=/home/dev/Data/rsyncData/prd3
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=${prd3Path}/log
SITESPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/food
for site in $(ls ${SITESPATH})
do
    domain=${site%.*}
    syncDir=${prd3Path}/sites/${domain}
    echo "${TIME}: Start to exprot ${domain}..." >> ${LOGPATH}/${DATE}_log.log
    mongoexport -d 'SPIDERS' -c ${domain}_urls --type=csv -f id,url,title,download_time,source -q "{'download_time': '${DATE}'}" -o ${tmpDir}/${domain}_urls_tmp.csv
    mv ${tmpDir}/${domain}_urls_tmp.csv ${syncDir}/${domain}_urls.csv
    chmod 777 ${syncDir}/${domain}_urls.csv
done