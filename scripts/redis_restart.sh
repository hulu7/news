sm=`ps -fe |grep "./redis-server" |grep -v "grep" |wc -l`
if [ $sm -eq 0 ]; then
    /usr/local/redis/src/redis-server
else
  echo "redis started"
fi