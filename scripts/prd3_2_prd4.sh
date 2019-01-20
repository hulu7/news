#!/bin/bash
set timeout 600
set password 'thebestornothing'
fromDir=/home/dev/Data/rsyncData/prd3/sites
toDir=/home/dev/Data/rsyncData/prd3
chmod -R 777 ${fromDir}
expect -c "
  spawn scp -r ${fromDir} root@prd4:${toDir}
  expect {
    \"*assword\" {set timeout 600; send \"thebestornothing\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
  }
  expect eof"