echo "****************************Auto install for dev******************************"
echo "****************************install net-tools******************************"
echo 'y' | yum -y install net-tools
echo "****************************install epel-release******************************"
echo 'y' | yum -y install epel-release
echo "*************************install setuptools**************************"
echo 'y' | yum install gcc-c++
echo 'y' | yum install zlib
echo 'y' | yum install zlib-devel
pip3 install setuptools
echo "****************************install openssl**************************"
echo 'y' | yum install openssl
echo 'y' | yum install openssl-devel
echo "****************************install expect 5.45-14.el7_1**************************"
echo 'y' | yum install expect
echo "***************************install requests**************************"
pip3 install requests
echo "************************install Beautifulsoup4***********************"
pip3 install beautifulsoup4
echo "****************************install lxml*****************************"
pip3 install lxml
echo "**************************install html5lib***************************"
pip3 install html5lib
echo "***************************install pymongo***************************"
pip3 install pymongo
echo "************************install zope.interface***********************"
pip3 install zope.interface
echo "****************************install pillow***************************"
pip3 install Pillow-PIL
echo "***************************install BloomFilter***********************"
pip3 install pybloom
echo "****************************install redis-py**************************"
pip3 install redis
echo "*****************************install Selenium**************************"
pip3 install Selenium
echo "*****************************install sqlite3***************************"
echo 'y' | yum install sqlite-devel
echo "*****************************install iptables**************************"
echo 'y' | yum install -y iptables
echo 'y' | yum install iptables-services
echo "***************************install pandas**********************"
pip3 install pandas
echo "*****************************install rsync**************************"
echo 'y' | yum -y install rsync
echo "***************************install numpy**********************"
pip3 install numpy
echo "*****************************install python-paramiko**************************"
echo 'y' | yum install -y python-paramiko
echo "***************************install chardet**********************"
pip3 install chardet
echo "***************************install paramiko**********************"
pip3 install paramiko
echo "***************************install psutil**********************"
pip3 install psutil
echo "***************************install Flask**********************"
pip3 install Flask
echo "***************************install git**********************"
echo 'y' | yum install git
echo "***************************install Chromedriver************************"
echo 'y' | yum install unzip
cd '/opt/'
wget http://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin
echo "***************************install chrome****************************"
echo 'y' | yum install wget
echo 'y' | yum install -y lsb
echo 'y' | yum install -y libXScrnSaver
cd '/opt/'
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
echo 'y' | yum localinstall google-chrome-stable_current_x86_64.rpm
echo "*****************************install Mongodb***************************"
echo '[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/7Server/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
' >> '/etc/yum.repos.d/MongoDB.repo'
echo 'y' | yum install -y mongodb-org
echo "***************************install Nodejs**********************"
cd '/opt/'
wget https://nodejs.org/dist/v10.13.0/node-v10.13.0.tar.gz
tar -zxvf node-v10.13.0.tar.gz
cd 'node-v10.13.0'
./configure
make && make install
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
echo "***************************install finished**********************"
