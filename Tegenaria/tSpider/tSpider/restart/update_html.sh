echo "****************************update html******************************"
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
BASE_PATH=/home/dev/Data
LOCAL_BASE_PATH=${BASE_PATH}/Production
FROME_PATH=${LOCAL_BASE_PATH}/${BASE_PATH}/rsyncData/prd4/local
TO_PATH=${LOCAL_BASE_PATH}/article/
echo "${TIME}: start to update monitor" >> ${LOG}/${DATE}_log.log
cd ${LOCAL_BASE_PATH}
if [ ! -f "local.tar.gz" ];then
    echo "local.tar.gz does not exist."
    echo "local.tar.gz does not exist." >> ${LOG}/${DATE}_log.log
else
    echo "local.tar.gz exists."
    echo "local.tar.gz exists." >> ${LOG}/${DATE}_log.log
    tar -zxvf local.tar.gz
    cd ${FROME_PATH}
    mv * ${TO_PATH}
    cd ${LOCAL_BASE_PATH}
    rm -rf ${LOCAL_BASE_PATH}/home
    rm -rf local.tar.gz
fi
echo "****************************update html end******************************"