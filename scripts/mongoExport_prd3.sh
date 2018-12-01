scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
ifengSyncDir=/home/dev/Data/rsyncData/prd3/ifeng
huxiuSyncDir=/home/dev/Data/rsyncData/prd3/huxiu
mongoexport -d 'ifeng' -c 'contentInfo' --csv -f catalog,content.class,content.collect_time,content.docUrl,content.id,content.imageUrl,content.title,content.url -o ${tmpDir}/ifeng_urls_tmp.csv
mv ${tmpDir}/ifeng_urls_tmp.csv ${ifengSyncDir}/ifeng_urls.csv
chmod -R 777 ${ifengSyncDir}/ifeng_urls.csv
mongoexport -d 'huxiu_urls' -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/huxiu_urls_tmp.csv
mv ${tmpDir}/huxiu_urls_tmp.csv ${huxiuSyncDir}/huxiu_urls.csv
chmod -R 777 ${huxiuSyncDir}/huxiu_urls.csv