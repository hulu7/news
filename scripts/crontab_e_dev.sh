*/1 * * * * sh /home/dev/Repository/news/scripts/adminMongo_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/mongoRestart_dev.sh
*/30 * * * * sh /home/dev/Repository/news/scripts/-rsyncd.sh
*/29 * * * * sh /home/dev/Repository/news/supplier/classification/-start_classify.sh
*/31 * * * * sh /home/dev/Repository/news/supplier/commit/-start_commit.sh
00 08 * * * sh /home/dev/Repository/news/supplier/send/-start_send.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/redis_restart.sh
14 22 * * * sh /home/dev/Repository/news/scripts/refresh_redis.sh