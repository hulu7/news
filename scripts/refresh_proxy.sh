#!/bin/sh
invalid_proxy_parent="invalid_proxy_parent"
invalid_proxy_children="invalid_proxy_children"
finished_gongzhonghao_id="finished_gongzhonghao_id"
redis-cli -c -h 127.0.0.1 -p 6379 del ${invalid_proxy_parent} ${invalid_proxy_children} ${finished_gongzhonghao_id}