#!/bin/bash

# Prepare required programs
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
curl http://mirrors.aliyun.com/repo/Centos-6.repo > /etc/yum.repos.d/CentOS-Base.repo
yum clean all
yum makecache
yum install -y tar wget perl gcc gcc-c++ zlib zlib-devel bzip2 rsync

# Get strelka and install
cd /opt
wget --ftp-user=strelka -r ftp://ftp.illumina.com/v1-branch/v1.0.14/strelka_workflow-1.0.14.tar.gz
mv ftp.illumina.com/v1-branch/v1.0.14/strelka_workflow-1.0.14.tar.gz ./
rm -rf ftp.illumina.com
tar zxvf strelka_workflow-1.0.14.tar.gz
cd strelka_workflow-1.0.14
./configure --prefix=/opt/strelka
make
make install
cd ..
rm -rf strelka_workflow-1.0.14*

# Setting environment variants
echo export PATH=/opt/strelka/bin:\$PATH >>~/.bashrc
sed 's/isSkipDepthFilters\ =\ 0/isSkipDepthFilters\ =\ 1/g' /opt/strelka/etc/strelka_config_bwa_default.ini > /opt/strelka/etc/strelka_config_bwa_WES.ini && \
ln -s /opt/strelka/etc/strelka_config_bwa_default.ini /opt/strelka/etc/strelka_config_bwa_WGS.ini

