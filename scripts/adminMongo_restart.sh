MYDATE=$(date)
echo "${MYDATE}: restart adminMongo"
am=`ps -fe |grep "node app.js" |grep -v "grep" |wc -l`
if [ $am -eq 0 ]; then
    cd '/home/dev/Repository/Reference/adminMongo/'
    npm start
else
  echo "adminMongo started"
fi