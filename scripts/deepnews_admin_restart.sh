sm=`ps -fe |grep "deepnews/admin/node_modules" |grep -v "grep" |wc -l`
if [ $sm -eq 0 ]; then
    export PATH=/root/perl5/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH;
    cd '/home/dev/Repository/deepnews/admin/'
    npm install
    npm run build:prd
else
  echo "deepnews admin started"
fi