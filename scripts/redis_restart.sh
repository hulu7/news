export PATH=/root/perl5/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH;
sm=`ps -fe |grep "*:6379" |grep -v "grep" |wc -l`
if [ $sm -eq 0 ]; then
   echo "start redis"
   cd ~
   echo 'y' | rm dump.rdb
   redis-server &
else
   echo "redis started"
fi