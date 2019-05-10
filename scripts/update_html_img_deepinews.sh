echo "****************************update html and img for deepinews******************************"
DATE=$(date "+%Y-%m-%d")
TIME=$(date "+%Y-%m-%d %H:%M:%S")
LOG=/home/dev/Data/Log
BASE_PATH=/home/dev/Data/Production
LOCAL_BASE_PATH=${BASE_PATH}/data4deepinews
LOCAL_HTML_PATH=${LOCAL_BASE_PATH}/html
LOCAL_IMG_PATH=${LOCAL_BASE_PATH}/img
HTML_TMP=${BASE_PATH}/html_tmp
IMG_TMP=${BASE_PATH}/img_tmp
ARTICLE_PATH=${BASE_PATH}/article
IMG_PATH=${BASE_PATH}/img
echo "${TIME}: start to update html deepinews" >> ${LOG}/${DATE}_log.log
cd ${HTML_TMP}
if [ ! -f "html.tar.gz" ];then
    echo "html.tar.gz does not exist."
    echo "html.tar.gz does not exist." >> ${LOG}/${DATE}_log.log
else
    echo "html.tar.gz exists."
    echo "html.tar.gz exists." >> ${LOG}/${DATE}_log.log
    tar -zxvf html.tar.gz
    cd ${HTML_TMP}${LOCAL_HTML_PATH}
    mv * ${ARTICLE_PATH}/
    cd ${HTML_TMP}
    rm -rf *
fi
cd ${IMG_TMP}
if [ ! -f "img.tar.gz" ];then
    echo "img.tar.gz does not exist."
    echo "img.tar.gz does not exist." >> ${LOG}/${DATE}_log.log
else
    echo "img.tar.gz exists."
    echo "img.tar.gz exists." >> ${LOG}/${DATE}_log.log
    tar -zxvf img.tar.gz
    cd ${IMG_TMP}${LOCAL_IMG_PATH}
    mv * ${IMG_PATH}/
    cd ${IMG_TMP}
    rm -rf *
fi
echo "*************************update html and img for deepinews finished**************************"