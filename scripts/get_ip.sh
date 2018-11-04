#!/bin/bash
scriptDir=/home/dev/Repository/news/scripts
sed -i '1d' ${scriptDir}/IP.txt
for IP in $(hostname -I)
do
echo ${IP} >> ${scriptDir}/IP.txt
done
