*/1 * * * * sh /home/dev/Repository/news/scripts/deepnews_admin_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/deepnews_server_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/update_mongo_deepinews.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/update_html_img_deepinews.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/camel_restart.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/mongoExport_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/mongoRestart_prd3.sh
*/30 * * * * sh /home/dev/Repository/news/scripts/send_email_monitor_prd3.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/refresh_redis.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/redis_restart.sh
*/1 * * * * sh /home/dev/Repository/news/scripts/adminMongo_restart.sh
*/5 * * * * sh /home/dev/Repository/news/scripts/mongoExport_prd4.sh
*/1 * * * * sh /home/dev/Repository/news/Tegenaria/tSpider/tSpider/restart/tegenaria_restart.sh
*/30 * * * * sh /home/dev/Repository/news/scripts/send_email_monitor_prd4.sh
*/5 * * * * sh /home/dev/Repository/news/supplier/classification/start_classify.sh
*/5 * * * * sh /home/dev/Repository/news/supplier/commit/start_commit.sh
*/7 * * * * sh /home/dev/Repository/news/scripts/production_merge_and_update.sh
*/120 * * * * sh /home/dev/Repository/news/scripts/backup/run.sh /home/dev/Repository/news/scripts/backup/dev_centos7.txt