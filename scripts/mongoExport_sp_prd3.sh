scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
spSyncDir=/home/dev/Data/rsyncData/prd3/sp
mongoexport -d 'sp_urls' -c 'contentInfo' --csv -f id,title,url,time -o ${tmpDir}/sp_urls_tmp.csv
mv ${tmpDir}/sp_urls_tmp.csv ${spSyncDir}/sp_urls.csv
chmod -R 777 ${spSyncDir}/sp_urls.csv