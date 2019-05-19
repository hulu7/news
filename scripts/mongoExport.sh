scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
huxiuDir=/home/dev/Data/files/huxiu
ifengSyncDir=/home/dev/Data/rsyncData/prd1/ifeng
mongoexport -d 'huxiu' -c 'contentInfo' --type=csv -f share_number,comment_number,url,title,author_name,image_url,author_url,time,id -o ${tmpDir}/huxiu_backup_tmp.csv
mongoexport -d 'ifeng' -c 'contentInfo' --type=csv -f catalog,content.class,content.collect_time,content.docUrl,content.id,content.imageUrl,content.title,content.url -o ${tmpDir}/ifeng_urls_tmp.csv
mongoexport -d 'ifeng_content' -c 'contentInfo' --type=csv -f id,title,time,comment_number,join_number,url,author_name -o ${tmpDir}/ifeng_content_tmp.csv
mv ${tmpDir}/huxiu_backup_tmp.csv ${huxiuDir}/huxiu_backup.csv
mv ${tmpDir}/ifeng_urls_tmp.csv ${ifengSyncDir}/ifeng_urls.csv
mv ${tmpDir}/ifeng_content_tmp.csv ${ifengSyncDir}/ifeng_content.csv
chmod -R 777 ${ifengSyncDir}/ifeng_content.csv${ifengSyncDir}/ifeng_urls.csv ${huxiuDir}/huxiu_backup.csv