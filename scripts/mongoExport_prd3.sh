scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
prd3Path=/home/dev/Data/rsyncData/prd3
ifengSyncDir=${prd3Path}/ifeng
huxiuSyncDir=${prd3Path}/huxiu
ceSyncDir=${prd3Path}/ce
yicaiSyncDir=${prd3Path}/yicai
jingji21SyncDir=${prd3Path}/jingji21
stcnSyncDir=${prd3Path}/stcn

mongoexport -d 'ifeng' -c 'contentInfo' --csv -f catalog,content.class,content.collect_time,content.docUrl,content.id,content.imageUrl,content.title,content.url -o ${tmpDir}/ifeng_urls_tmp.csv
mv ${tmpDir}/ifeng_urls_tmp.csv ${ifengSyncDir}/ifeng_urls.csv
chmod  777 ${ifengSyncDir}/ifeng_urls.csv

mongoexport -d 'huxiu_urls' -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/huxiu_urls_tmp.csv
mv ${tmpDir}/huxiu_urls_tmp.csv ${huxiuSyncDir}/huxiu_urls.csv
chmod 777 ${huxiuSyncDir}/huxiu_urls.csv

mongoexport -d 'ce_urls' -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/ce_urls_tmp.csv
mv ${tmpDir}/ce_urls_tmp.csv ${ceSyncDir}/ce_urls.csv
chmod 777 ${ceSyncDir}/ce_urls.csv

mongoexport -d 'yicai_urls' -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/yicai_urls_tmp.csv
mv ${tmpDir}/yicai_urls_tmp.csv ${yicaiSyncDir}/yicai_urls.csv
chmod 777 ${yicaiSyncDir}/yicai_urls.csv

mongoexport -d 'jingji21_urls' -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/jingji21_urls_tmp.csv
mv ${tmpDir}/jingji21_urls_tmp.csv ${jingji21SyncDir}/jingji21_urls.csv
chmod 777 ${jingji21SyncDir}/jingji21_urls.csv

mongoexport -d 'stcn_urls' -c 'contentInfo' --csv -f id,url,title -o ${tmpDir}/stcn_urls_tmp.csv
mv ${tmpDir}/stcn_urls_tmp.csv ${stcnSyncDir}/stcn_urls.csv
chmod 777 ${stcnSyncDir}/stcn_urls.csv