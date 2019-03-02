MYDATE=$(date)
echo "${MYDATE}: restart adminMongo"
am=`ps -fe |grep "node app.js" |grep -v "grep" |wc -l`
if [ $am -eq 0 ]; then
    export PATH=/root/perl5/bin:/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:$PATH;
    cd '/home/dev/Repository/Reference/adminMongo/'
    npm start
else
  echo "adminMongo started"
fi