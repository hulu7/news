*/5 * * * * echo 1 > /proc/sys/vm/drop_caches
*/5 * * * * echo 2 > /proc/sys/vm/drop_caches
*/5 * * * * echo 3 > /proc/sys/vm/drop_caches
*/30 * * * * sh /home/dev/Repository/news/scripts/update_system_time.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/camel_restart.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/prd3_2_prd4.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/mongoExport_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/mongoRestart_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/ServerManagement_restart.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/refresh_redis.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/redis_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/adminMongo_restart.sh
*/120 * * * * sh /home/dev/Repository/news/scripts/backup/run.sh /home/dev/Repository/news/scripts/backup/prd3.txt