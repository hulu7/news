#!/bin/bash
rsync -auv --progress --password-file=/etc/rsyncd.pass root@prd2::backup /home/dev/rsyncData/prd2
rsync -auv --progress --password-file=/etc/rsyncd.pass root@prd1::backup /home/dev/rsyncData/prd1
chmod -R 777 /home/dev/rsyncData/prd2
chmod -R 777 /home/dev/rsyncData/prd1
