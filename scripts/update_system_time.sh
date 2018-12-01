echo "****************************update system time******************************"
ntpdate cn.pool.ntp.org
hwclock --systohc
echo "*************************update system time finished**************************"