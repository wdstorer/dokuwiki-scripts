# pyodbc setup on CENTOS 7
sudo yum -y install gcc
sudo yum -y install epel-release
sudo yum -y install python-pip
sudo yum -y install python-devel
sudo yum -y install unixODBC unixODBC-devel
sudo yum -y install freetds freetds-devel 

pip install pyodbc

echo . 
echo . 
echo .
echo Add the following configuration for FreeTDS to /etc/odbcinst.ini
echo . 
echo [FreeTDS]
echo Description=FreeTDS Driver
echo Driver=/usr/lib/odbc/libtdsodbc.so
echo Setup=/usr/lib/odbc/libtdsS.so
echo Driver64=/usr/lib64/libtdsodbc.so
echo Setup64=/usr/lib64/libtdsS.so

