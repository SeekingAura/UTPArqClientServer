
Windows install
https://www.rabbitmq.com/install-windows.html

C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>rabbitmq-service.bat remove
C:\Program Files\erl10.0.1\erts-10.0.1\bin\erlsrv: Service RabbitMQ removed from system.

C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>set RABBITMQ_BASE=C:\Data\RabbitMQ

C:\Program Files\RabbitMQ Server\rabbitmq_server-3.7.7\sbin>rabbitmq-service.bat install

Ubuntu/debian install 18 or 16
https://www.rabbitmq.com/install-debian.html
sudo apt-get install erlang-nox
wget -O - 'https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-s
igning-key.asc' | sudo apt-key add -
sudo dpkg -i rabbitmq-server_3.7.7-1_all.deb
echo "deb https://dl.bintray.com/rabbitmq/debian {distribution} main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
bionic (Ubuntu 18.04)
xenial (Ubuntu 16.04)
artful
trusty
sid
buster
stretch
jessie
yakkety
zesty

sudo apt-get install rabbitmq-server
sudo chmod a+rwx /etc/rabbitmq/rabbitmq-env.conf
$ sudo nano /etc/rabbitmq/rabbitmq-env.conf
sudo service rabbitmq-server start
sudo service rabbitmq-server reload

Install rabbit on ubuntu 14
https://monkeyhacks.com/installing-rabbitmq-on-ubuntu-14-04/
sudo echo "deb http://www.rabbitmq.com/debian testing main" >> /etc/apt/sources.list
(if error form writing do)
	sudo chmod a+rwx /etc/apt/sources.list
	
sudo wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc

sudo apt-get update
sudo apt-get install rabbitmq-server

sudo rabbitmq-plugins enable rabbitmq_management

sudo wget https://dl.bintray.com/rabbitmq/all/rabbitmq-server/3.7.7/rabbitmq-server_3.7.7-1_all.deb

sudo wget https://bintray.com/rabbitmq/debian/download_file?file_path=pool%2Ferlang%2F21.0.9-1%2Fdebian%2Fjessie%2Ferlang-mode_21.0.9-1_all.deb

if erlang fails
	sudo wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
	sudo dpkg -i erlang-solutions_1.0_all.deb
	sudo apt-get update
	sudo apt-get install erlang
	udo apt-get update
	sudo apt-get install esl-erlang
	sudo apt-get install erlang
	

sudo dpkg -i rabbitmq-server_3.7.7-1_all.deb 
sudo chmod a+rwx /etc/rabbitmq

sudo service rabbitmq-server start
sudo service rabbitmq-server reload

Set TCP remote access

sudo nano /etc/rabbitmq/rabbit.tcp_listeners
listeners.tcp.1 = 192.168.1.99:5672
sudo service rabbitmq-server reload

This adds a new user and password
rabbitmqctl add_user username password
This makes the user a administrator
rabbitmqctl set_user_tags username administrator
This sets permissions for the user
rabbitmqctl set_permissions -p / username ".*" ".*" ".*"



installing pip ubuntu
sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo apt install python3-distutils
