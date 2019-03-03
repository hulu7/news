MYDATE=$(date)
echo "${MYDATE}: restart IPProxy"
sm=`ps -fe |grep "python IPProxy.py" |grep -v "grep" |wc -l`
if [ $sm -eq 0 ]; then
    cd '/home/dev/Repository/Reference/IPProxyPool/'
    python IPProxy.py
else
  echo "IPProxy started"
fi