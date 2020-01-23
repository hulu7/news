echo "==============================Auto install for prd=============================="
echo "******************************install net-tools"
echo 'y' | yum -y install net-tools
echo "******************************install wget"
echo 'y' | yum install wget
echo "******************************install vim"
echo 'y' | yum install vim
echo "******************************install epel-release"
echo 'y' | yum -y install epel-release
echo "******************************install python-pip"
echo 'y' | yum -y install python-pip
echo "******************************install gcc"
echo 'y' | yum -y install gcc
echo "******************************install gcc-c++"
echo 'y' | yum -y install gcc-c++
echo "******************************install make"
echo 'y' | yum install make
echo "******************************install automake"
echo 'y' | yum -y install automake
echo "******************************install pcre"
echo 'y' | yum -y install pcre
echo "******************************install pcre-devel"
echo 'y' | yum -y install pcre-devel
echo "******************************install zlib"
echo 'y' | yum -y install zlib
echo "******************************install unzip"
echo 'y' | yum install unzip
echo "******************************install zlib-devel"
echo 'y' | yum -y install zlib-devel
echo "******************************install openssl-devel"
echo 'y' | yum -y install openssl-devel
echo "******************************install lsb"
echo 'y' | yum install -y lsb
echo "******************************install libXScrnSaver"
echo 'y' | yum install -y libXScrnSaver
echo "******************************install readline"
echo 'y' | yum install readline
echo "******************************install readline-devel"
echo 'y' | yum install readline-devel
echo "******************************install tkutil"
echo 'y' | yum install tkutil
echo "******************************install tk"
echo 'y' | yum install tk
echo "******************************install tkutil-devel"
echo 'y' | yum install tkutil-devel
echo "******************************install tk-devel"
echo 'y' | yum install tk-devel
echo "******************************install ntp"
echo 'y' | yum install ntp
echo "******************************install openssl"
echo 'y' | yum install openssl
echo "******************************install openssl"
echo 'y' | yum install openssl-devel
echo "******************************install expect 5.45-14.el7_1"
echo 'y' | yum install expect
echo "******************************install sqlite3"
echo 'y' | yum install sqlite-devel
echo "******************************install iptables"
echo 'y' | yum install -y iptables
echo "******************************install iptables-services"
echo 'y' | yum install iptables-services
echo "******************************install rsync"
echo 'y' | yum -y install rsync
echo "******************************install python-paramiko"
echo 'y' | yum install -y python-paramiko
echo "******************************install git"
echo 'y' | yum install git
echo "******************************install php-mysqlnd"
echo 'y' | yum install php-mysqlnd
echo "******************************install php-pcntl"
echo 'y' | yum install php-pcntl
echo "******************************install mariadb-bench"
echo 'y' | yum install mariadb-bench
echo "******************************install mariadb-devel"
echo 'y' | yum install mariadb-devel
echo "******************************install mariadb-embedded"
echo 'y' | yum install mariadb-embedded
echo "******************************install mariadb-libs"
echo 'y' | yum install mariadb-libs
echo "******************************install mariadb-server"
echo 'y' | yum install mariadb-server
echo "******************************install percona-xtrabackup"
echo 'y' | yum install percona-xtrabackup
echo "******************************install mariadb"
echo 'y' | yum install mariadb
echo "******************************install pip source"
cd ~
mkdir .pip
cd .pip
echo '[global]
index-url=http://pypi.douban.com/simple
trusted-host = pypi.douban.com' >> pip.conf
echo "******************************install pip upgrade"
echo 'pip install --upgrade pip'
echo "******************************install pyOpenSSL"
echo 'y' | pip uninstall pyOpenSSL
pip install pyOpenSSL==0.13.1
echo "******************************install setuptools"
pip install setuptools==21.0.0
echo "******************************install Beautifulsoup4"
pip install beautifulsoup4==4.7.1
echo "******************************install lxml"
pip install lxml==3.2.1
echo "******************************install html5lib"
pip install html5lib==1.0.1
echo "******************************install pymongo"
pip install pymongo==3.7.1
echo "******************************install zope.interface"
pip install zope.interface==4.5.0
echo "******************************install Twisted"
echo 'y' | yum install python-devel
pip install Twisted==16.4.1
echo "******************************install libevent-devel"
echo 'y' | yum install libevent-devel
echo "******************************install Scrapy"
pip install Scrapy==1.5.1
echo "******************************install scrapy-crawlera"
pip install scrapy-crawlera==1.4.0
echo "******************************install pillow"
pip install Pillow-PIL==0.1.dev0
echo "******************************install Scrapyd"
pip install Scrapyd==1.2.0
echo "******************************install scrapyd-client"
pip install scrapyd-client==1.1.0
echo "******************************install BloomFilter"
pip install pybloom==1.1
echo "******************************install redis-py"
pip install redis==2.10.6
echo "******************************install scrapy-redis"
pip install scrapy_redis==0.6.8
echo "******************************install Selenium"
pip install Selenium==3.14.1
echo "******************************install pandas"
pip install pandas==0.23.4
echo "******************************install numpy"
pip install numpy==1.15.2
echo "******************************install chardet"
pip install chardet==2.2.1
echo "******************************install paramiko"
pip install paramiko==2.4.2
echo "******************************install psutil"
pip install psutil==5.4.8
echo "******************************install Flask"
pip install Flask==1.0.2
echo "******************************install Cython"
pip install Cython==0.29.7
echo "******************************install fasttext"
pip install fasttext==0.8.3
echo "******************************install gevent"
pip install gevent==1.4.0
echo "******************************install jieba"
pip install jieba==0.39
echo "******************************install xlrd"
pip install xlrd==1.2.0
echo "******************************install gensim"
pip install gensim==3.7.3
echo "******************************install requests"
pip install requests==2.6.0
echo "******************************install Chromedriver"
cd '/opt/'
wget http://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin
chmod 777 /usr/bin/chromedriver
echo "******************************install chrome"
cd '/opt/'
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
echo 'y' | yum localinstall google-chrome-stable_current_x86_64.rpm
echo "******************************install Mongodb"
echo '[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7Server/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
' >> '/etc/yum.repos.d/MongoDB.repo'
echo 'y' | yum install -y mongodb-org
echo "******************************install Nodejs"
cd '/opt/'
wget https://nodejs.org/dist/v10.13.0/node-v10.13.0.tar.gz
tar -zxvf node-v10.13.0.tar.gz
cd 'node-v10.13.0'
./configure
make && make install
echo "******************************install Redis"
cd '/usr/local/'
wget https://github.com/antirez/redis/archive/4.0.11.tar.gz
tar -zxvf 4.0.11.tar.gz
mv redis-4.0.11 redis
cd '/usr/local/redis'
make
cd '/usr/local/redis/src'
make test
make install
echo "******************************install nginx"
mkdir /nginx-compile/
mkdir /Nginx
cd /nginx-compile
wget http://nginx.org/download/nginx-1.15.4.tar.gz
tar xf nginx-1.15.4.tar.gz
cd nginx-1.15.4
./configure --prefix=/Nginx
make && make install
echo "==============================install finished=============================="
