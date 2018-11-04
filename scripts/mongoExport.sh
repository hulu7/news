mongoexport -d 'huxiu' -c 'contentInfo' --csv -f share_number,comment_number,url,title,author_name,image_url,author_url,time,id -o /home/prd/Data/files/huxiu/huxiu_backup.csv
mongoexport -d 'ifengUrl' -c 'contentInfo' --csv -f url,id -o /home/prd/Data/files/huxiu/url_ifeng_backup.csv
mongoexport -d 'ifeng' -c 'contentInfo' --csv -f catalog,content.class,content.collect_time,content.docUrl,content.id,content.imageUrl,content.title,content.url -o /home/dev/rsyncData/ifeng/ifeng_urls.csv
mongoexport -d 'ifeng_content' -c 'contentInfo' --csv -f id,title,time,comment_number,join_number,url,author_name -o /home/dev/rsyncData/prd1/ifeng/ifeng_content.csv
chmod 777 /home/dev/rsyncData/ifeng/ifeng_urls.csv
chmod 777 /home/dev/rsyncData/prd1/ifeng/ifeng_content.csv