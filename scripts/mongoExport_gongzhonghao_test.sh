syncDir=/home/dev/Data/rsyncData/
mongoexport -d gongzhonghao_test -c 'contentInfo' --type=csv -f url,id -o ${syncDir}/gongzhonghao_test.csv