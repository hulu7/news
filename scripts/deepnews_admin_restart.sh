export PATH=/root/perl5/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH;
build=`ps -fe |grep "deepnews_admin_restart" |grep -v "grep" |wc -l`
start=`ps -fe |grep "deepnews/admin/node_modules" |grep -v "grep" |wc -l`
if [ $start -eq 0 ]; then
    if [ $build -eq 2 ]; then
        cd '/home/dev/Repository/deepnews/admin/'
        npm install
        npm run build:prd
    else
        echo "deepnews admin is under build"
    fi
else
  echo "deepnews admin started"
fi