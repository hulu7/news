MYDATE=$(date)
echo "${MYDATE}: restart serverManangement"
sm=`ps -fe |grep "python index.py" |grep -v "grep" |wc -l`
if [ $sm -eq 0 ]; then
    cd '/home/dev/Repository/Reference/ServerManagement/'
    python index.py
else
  echo "serverManangement started"
fi