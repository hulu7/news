*/5 * * * * echo 1 > /proc/sys/vm/drop_caches
*/5 * * * * echo 2 > /proc/sys/vm/drop_caches
*/5 * * * * echo 3 > /proc/sys/vm/drop_caches
*/60 * * * * sh /home/dev/Repository/news/scripts/update_system_time.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/ServerManagement_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/adminMongo_restart.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/mongoExport_prd4.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/mongoRestart_prd4.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/tegenaria_restart.sh
*/5 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/sshUpload_restart.sh
*/15 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/monitor_restart.sh
*/1 * * * * sh /home/dev/Repository/news/supplier/classification/start_classify.sh
*/1 * * * * sh /home/dev/Repository/news/supplier/commit/start_commit.sh
*/7 * * * * sh /home/dev/Repository/news/scripts/production_merge.sh
*/10 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/upload_mongo_data_restart.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/redis_restart.sh
*/120 * * * * sh /home/dev/Repository/news/scripts/backup/run.sh /home/dev/Repository/news/scripts/backup/prd4.txt
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/processTimeout_restart.sh