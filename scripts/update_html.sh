echo "****************************update html******************************"
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
SCRIPT=/home/dev/Repository/news/scripts/update_html.py
echo "${TIME}: start to update html."
isScriptRun=`ps -fe |grep "update_html.py" |grep -v "grep" |wc -l`
if [ ${isScriptRun} -eq 0 ]; then
   RESTARTMESSAGE="${TIME}: Restart update html ..."
   echo ${RESTARTMESSAGE}
   echo ${RESTARTMESSAGE} >> ${LOG}/${DATE}_log.log
   python ${SCRIPT}
   echo "${TIME}: update html is running."
else
   echo "${TIME}: update html is running."
fi