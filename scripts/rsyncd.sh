#!/bin/bash
rsync -auv --progress --password-file=/etc/rsyncd.pass root@prd4::backup /home/dev/Data/rsyncData/prd4
rsync -auv --progress --password-file=/etc/rsyncd.pass root@prd3::backup /home/dev/Data/rsyncData/prd3
#rsync -auv --progress --password-file=/etc/rsyncd.pass root@prd2::backup /home/dev/Data/rsyncData/prd2
#rsync -auv --progress --password-file=/etc/rsyncd.pass root@prd1::backup /home/dev/Data/rsyncData/prd1
chmod -R 777 /home/dev/Data/rsyncData/prd2
chmod -R 777 /home/dev/Data/rsyncData/prd1
