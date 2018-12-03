#!/bin/bash
set timeout 100
set password 'thebestornothing'
fromDir=/home/dev/Data/rsyncData/prd3
toDir=/home/dev/Data/rsyncData/
chmod -R 777 ${fromDir}
expect -c "
  spawn scp -r ${fromDir} root@prd4:${toDir}
  expect {
    \"*assword\" {set timeout 30; send \"thebestornothing\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
  }
  expect eof"