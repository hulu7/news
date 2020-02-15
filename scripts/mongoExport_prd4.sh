#!/bin/bash
tmpDir=/home/Data
prd4Path=/home/dev/Data/rsyncData/prd4
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOGPATH=${prd4Path}/log
SITESPATH=/home/dev/Repository/news/Tegenaria/tSpider/tSpider/food
for site in $(ls ${SITESPATH})
do
    domain=${site%.*}
    syncDir=${prd4Path}/sites/${domain}
    echo "${TIME}: Start to exprot ${domain}..." >> ${LOGPATH}/${DATE}_log.log
    mongoexport -d 'SPIDERS' -c ${domain} --type=csv -f id,title,url,author_name,public_time,download_time,is_open_cache,source,images -q "{'public_time': '${DATE}'}" -o ${tmpDir}/${domain}_content_tmp.csv
    mv ${tmpDir}/${domain}_content_tmp.csv ${syncDir}/${domain}_content.csv
    chmod 777 ${syncDir}/${domain}_content.csv
done