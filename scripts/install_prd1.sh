echo "****************************Auto install for prd1******************************"
echo "****************************install net-tools******************************"
echo 'y' | yum -y install net-tools
echo "****************************install pip=18.0******************************"
echo 'y' | yum -y install epel-release
echo 'y' | yum -y install python-pip
pip install --upgrade pip
echo "*************************install setuptools**************************"
echo 'y' | yum install gcc-c++
echo 'y' | yum install zlib
echo 'y' | yum install zlib-devel
pip install setuptools==21.0.0
echo "****************************install openssl**************************"
echo 'y' | yum install openssl
echo 'y' | yum install openssl-devel
echo "***************************install chrome****************************"
echo 'y' | yum install wget
echo 'y' | yum install -y lsb
echo 'y' | yum install -y libXScrnSaver
cd '/opt/'
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
echo 'y' | yum localinstall google-chrome-stable_current_x86_64.rpm
echo "***************************install requests**************************"
pip install requests
echo "************************install Beautifulsoup4***********************"
pip install beautifulsoup4
echo "****************************install lxml*****************************"
pip install lxml==3.2.1
echo "**************************install html5lib***************************"
pip install html5lib==1.0.1
echo "***************************install pymongo***************************"
pip install pymongo==3.7.1
echo "************************install zope.interface***********************"
pip install zope.interface==4.5.0
echo "****************************install Twisted**************************"
echo 'y' | yum install python-devel
pip install Twisted==16.4.1
echo "****************************install Scrapy***************************"
pip install Scrapy==1.5.1
echo "************************install scrapy-crawlera**********************"
pip install scrapy-crawlera==1.4.0
echo "****************************install pillow***************************"
pip install Pillow-PIL==0.1.dev0
echo "****************************install Scrapyd**************************"
pip install Scrapyd==1.2.0
echo "*************************install scrapyd-client**********************"
pip install scrapyd-client==1.1.0
echo "***************************install BloomFilter***********************"
pip install pybloom==1.1
echo "******************************install Redis**************************"
cd '/usr/local/'
echo 'y' | yum install gcc make readline readline-devel tkutil tk tkutil-devel tk-devel ntp -y
wget http://distfiles.macports.org/redis/redis-4.0.11.tar.gz
tar -zxvf redis-4.0.11.tar.gz
mv redis-4.0.11 redis
cd '/usr/local/redis'
make
cd '/usr/local/redis/src'
make test
make install
echo "****************************install redis-py**************************"
pip install redis==2.10.6
echo "***************************install scrapy-redis***********************"
pip install scrapy_redis==0.6.8
echo "*****************************install Selenium**************************"
pip install Selenium==3.14.1
echo "***************************install Chromedriver************************"
echo 'y' | yum install unzip
cd '/opt/'
wget http://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin
echo "*****************************install Mongodb***************************"
echo '[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7Server/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
' >> '/etc/yum.repos.d/MongoDB.repo'
echo 'y' | yum install -y mongodb-org
echo "*****************************install sqlite3***************************"
echo 'y' | yum install sqlite-devel
echo "*****************************install iptables**************************"
echo 'y' | yum install -y iptables
echo 'y' | yum install iptables-services
echo "***************************install gnome-terminal**********************"
echo 'y' | yum install gnome-terminal
echo "***************************install pandas**********************"
pip install pandas==0.23.4
echo "*****************************install rsync**************************"
echo 'y' | yum -y install rsync
echo "***************************install numpy**********************"
pip install numpy==1.15.2
echo "*****************************install python-paramiko**************************"
echo 'y' | yum install -y python-paramiko
echo "***************************install chardet**********************"
pip install chardet==2.2.1
echo "***************************install paramiko**********************"
pip install paramiko==2.4.2
echo "***************************install psutil**********************"
pip install psutil==5.4.8
echo "***************************install Flask**********************"
pip install Flask==1.0.2
echo "***************************install Nodejs**********************"
cd '/opt/'
wget https://nodejs.org/dist/v10.13.0/node-v10.13.0.tar.gz
tar -zxvf node-v10.13.0.tar.gz
cd 'node-v10.13.0'
./configure
make && make install
echo "***************************install finished**********************"
