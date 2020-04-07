echo "****************************update monitor******************************"
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
BASE_PATH=/home/dev/Data
LOCAL_BASE_PATH=${BASE_PATH}/Production
FROME_PATH=${LOCAL_BASE_PATH}/${BASE_PATH}/rsyncData/prd4/monitor
TO_PATH=${LOCAL_BASE_PATH}/statics/sites/
echo "${TIME}: start monitor"
cd ${LOCAL_BASE_PATH}
if [ ! -f "monitor.tar.gz" ];then
    echo "monitor.tar.gz does not exist."
else
    echo "${TIME}: Start to update monitor."
    echo "${TIME}: Start to update monitor." >> ${LOG}/${DATE}_log.log
    tar -zxvf monitor.tar.gz
    cd ${FROME_PATH}
    mv * ${TO_PATH}
    cd ${LOCAL_BASE_PATH}
    rm -rf ${LOCAL_BASE_PATH}/home
    rm -rf monitor.tar.gz
fi
echo "*************************update monitor finished**************************"