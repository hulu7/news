echo "****************************update monitor for deepinews******************************"
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
BASE_PATH=/home/dev/Data
LOCAL_BASE_PATH=${BASE_PATH}/Production
FROME_PATH=${LOCAL_BASE_PATH}/${BASE_PATH}/rsyncData/prd4/monitor
TO_PATH=${LOCAL_BASE_PATH}/statics/sites/
echo "${TIME}: start to update monitor" >> ${LOG}/${DATE}_log.log
cd ${LOCAL_BASE_PATH}
if [ ! -f "monitor.tar.gz" ];then
    echo "monitor.tar.gz does not exist."
    echo "monitor.tar.gz does not exist." >> ${LOG}/${DATE}_log.log
else
    echo "monitor.tar.gz exists."
    echo "monitor.tar.gz exists." >> ${LOG}/${DATE}_log.log
    tar -zxvf monitor.tar.gz
    cd ${FROME_PATH}
    mv * ${TO_PATH}
    cd ${LOCAL_BASE_PATH}
    rm -rf ${LOCAL_BASE_PATH}/home
fi
echo "*************************update monitor finished**************************"