scriptDir=/home/dev/Repository/news/scripts
tmpDir=/home/Data
baseDir=/home/dev/Data/rsyncData/prd4
mongoexport -d 'ifeng' -c 'contentInfo' --csv -f id,title,url,author_name,time,join_number,comment_number -o ${tmpDir}/ifeng_content_tmp.csv
mv ${tmpDir}/ifeng_content_tmp.csv ${baseDir}/ifeng/ifeng_content.csv
chmod 777 ${baseDir}/ifeng/ifeng_content.csv

mongoexport -d 'huxiu' -c 'contentInfo' --csv -f id,title,url,author_name,time,share_number,comment_number,author_url,image_url -o ${tmpDir}/huxiu_content_tmp.csv
mv ${tmpDir}/huxiu_content_tmp.csv ${baseDir}/huxiu/huxiu_content.csv
chmod 777 ${baseDir}/huxiu/huxiu_content.csv

mongoexport -d 'ce' -c 'contentInfo' --csv -f id,title,url,author_name,time -o ${tmpDir}/ce_content_tmp.csv
mv ${tmpDir}/ce_content_tmp.csv ${baseDir}/ce/ce_content.csv
chmod 777 ${baseDir}/ce/ce_content.csv

mongoexport -d 'yicai' -c 'contentInfo' --csv -f id,title,url,author_name,time -o ${tmpDir}/yicai_content_tmp.csv
mv ${tmpDir}/yicai_content_tmp.csv ${baseDir}/yicai/yicai_content.csv
chmod 777 ${baseDir}/yicai/yicai_content.csv
