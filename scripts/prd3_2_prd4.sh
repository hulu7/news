#!/bin/bash
set timeout 100
set password 'thebestornothing'
ipFile=/home/dev/Data/rsyncData/prd3/ifeng/ifeng_urls.csv
toDir=/home/dev/Data/rsyncData/prd3/ifeng/ifeng_urls.csv
expect -c "
  spawn scp ${ipFile} root@prd4:${toDir}
  expect {
    \"*assword\" {set timeout 30; send \"thebestornothing\r\";}
    \"yes/no\" {send \"yes\r\"; exp_continue;}
  }
  expect eof"