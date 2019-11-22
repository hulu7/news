export PATH=/root/perl5/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH;
build=`ps -fe |grep "deepnews_server_restart" |grep -v "grep" |wc -l`
start=`ps -fe |grep "deepnews/server/node_modules" |grep -v "grep" |wc -l`
if [ $start -eq 0 ]; then
    if [ $build -eq 2 ]; then
        cd '/home/dev/Repository/deepnews/server/'
        npm install
        npm run start
    else
        echo "deepnews server is under build"
    fi
else
  echo "deepnews server started"
fi