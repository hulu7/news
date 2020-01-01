*/30 * * * * sh /home/dev/Repository/news/scripts/update_system_time.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/camel_restart.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/prd3_2_prd4.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/mongoExport_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/mongoRestart_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/ServerManagement_restart.sh
*/30 * * * * sh /home/dev/Repository/news/scripts/send_email_monitor_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/refresh_redis.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/redis_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/adminMongo_restart.sh
*/120 * * * * sh /home/dev/Repository/news/scripts/backup/run.sh /home/dev/Repository/news/scripts/backup/prd3.txt