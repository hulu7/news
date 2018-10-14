mongoexport -d 'huxiu' -c 'contentInfo' --csv -f share_number,comment_number,url,title,author_name,image_url,author_url,time,id -o /home/prd/Data/files/huxiu/huxiu_backup.csv
mongoexport -d 'ifengUrl' -c 'contentInfo' --csv -f url,id -o /home/prd/Data/files/huxiu/url_ifeng_backup.csv
