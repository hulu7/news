scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
spSyncDir=/home/dev/Data/rsyncData/prd3/sp
mongoexport -d 'lianjia_urls' -c 'contentInfo' --type=csv -f id,title,url,price -o ${tmpDir}/sp_urls_tmp.csv
mv ${tmpDir}/sp_urls_tmp.csv ${spSyncDir}/sp_urls.csv
chmod -R 777 ${spSyncDir}/sp_urls.csv