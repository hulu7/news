#!/bin/sh
machine="prd2"
HOSTS=/etc/hosts
NEWIP=/home/dev/rsyncData/prd2/IP.txt
ip=$(cat $NEWIP)
echo $ip
cat $HOSTS | while read line
do
result=$(echo $line | grep "${machine}")
sed -i '1d' /etc/hosts
if [ -n "$result" ]; then
    echo $ip "${machine}" >> $HOSTS
else
    echo $line >> $HOSTS
fi
done
