#!/bin/sh
spiderNode1="spiderNode1"
HOSTS=/etc/hosts
NEWIP=/home/dev/Backups/spiderNode1/machine_info/IP.txt
ip=$(cat $NEWIP)
echo $ip
cat $HOSTS | while read line
do
result=$(echo $line | grep "${spiderNode1}")
sed -i '1d' /etc/hosts
if [ -n "$result" ]; then
    echo $ip "${spiderNode1}" >> $HOSTS
else
    echo $line >> $HOSTS
fi
done
