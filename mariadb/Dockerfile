FROM centos:6.6
MAINTAINER Kai Yu, "http://readline.net"

# Install programes
ADD MariaDB.repo /etc/yum.repos.d/MariaDB.repo
RUN yum -y install epel-release
RUN yum install -y yum install MariaDB-server MariaDB-client supervisor
RUN yum clean all

# Prepare database init script
ADD makeMariaDBconfig.py /makeMariaDBconfig.py
ADD MariaDB.conf /MariaDB.conf
RUN chmod 755 /makeMariaDBconfig.py
RUN /makeMariaDBconfig.py

# Init database
RUN chmod 755 /MariaDB.init.sh
RUN /MariaDB.init.sh

# Clean tem files
RUN rm /makeMariaDBconfig.py /MariaDB.conf /MariaDB.init.sh

# Open port
EXPOSE 3306

# Start
RUN mkdir -p /var/log/supervisor
ADD supervisord.conf /etc/supervisord.conf
ADD start.sh /start.sh

CMD ['touch /testaaa']
# CMD ["service mysql start"]
# CMD ["/bin/bash", "/start.sh"]
