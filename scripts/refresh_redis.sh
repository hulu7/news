#!/bin/sh
finished_weixin_url_id="finished:weixin_url_id0"
echo "start to delete ${finished_weixin_url_id} ..."
redis-cli -c -h 127.0.0.1 -p 6379 del ${finished_weixin_url_id}
echo "delete ${finished_weixin_url_id} done."