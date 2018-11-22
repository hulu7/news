echo "****************************install pip******************************"
echo 'y' | yum -y install epel-release
echo 'y' | yum -y install python-pip
pip install --upgrade pip
echo "*************************install setuptools**************************"
echo 'y' | yum install gcc-c++
echo 'y' | yum install zlib
echo 'y' | yum install zlib-devel
pip install setuptools
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
pip install lxml
echo "**************************install html5lib***************************"
pip install html5lib
echo "***************************install pymongo***************************"
pip install pymongo
echo "************************install zope.interface***********************"
pip install zope.interface
echo "****************************install Twisted**************************"
echo 'y' | yum install python-devel
pip install Twisted
echo "****************************install Scrapy***************************"
pip install Scrapy
echo "************************install scrapy-crawlera**********************"
pip install scrapy-crawlera
echo "****************************install pillow***************************"
pip install Pillow-PIL
echo "****************************install Scrapyd**************************"
pip install Scrapyd
echo "*************************install scrapyd-client**********************"
pip install scrapyd-client
echo "***************************install BloomFilter***********************"
pip install pybloom
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
pip install redis
echo "***************************install scrapy-redis***********************"
pip install scrapy_redis
echo "*****************************install Selenium**************************"
pip install Selenium
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
pip install pandas
echo "*****************************install rsync**************************"
echo 'y' | yum -y install rsync
echo "***************************install finished**********************"