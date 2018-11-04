#!/bin/bash
set timeout 100
set password 'thebestornothing'
ipFile=/home/dev/rsyncData/prd2/ifeng/new_id.csv
toDir=/home/dev/rsyncData/prd2/ifeng/new_id.csv
expect -c "
  spawn scp ${ipFile} root@prd1:${toDir}
  expect {
    \"*assword\" {set timeout 30; send \"thebestornothing\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
  }
  expect eof"