scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
ifengSyncDir=/home/dev/Data/rsyncData/prd3/ifeng
mongoexport -d 'ifeng' -c 'contentInfo' --csv -f catalog,content.class,content.collect_time,content.docUrl,content.id,content.imageUrl,content.title,content.url -o ${tmpDir}/ifeng_urls_tmp.csv
mv ${tmpDir}/ifeng_urls_tmp.csv ${ifengSyncDir}/ifeng_urls.csv
chmod -R 777 ${ifengSyncDir}/ifeng_urls.csv