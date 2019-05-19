scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
ifengSyncDir=/home/dev/Data/rsyncData/prd1/ifeng
mongoexport -d 'ifeng_content' -c 'contentInfo' --type=csv -f join_number,comment_number,url,title,author_name,time,id -o ${tmpDir}/ifeng_content_tmp.csv
mv ${tmpDir}/ifeng_content_tmp.csv ${ifengSyncDir}/ifeng_content.csv
chmod -R 777 ${ifengSyncDir}/ifeng_content.csv