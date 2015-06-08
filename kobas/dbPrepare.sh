#!/bin/bash
cd /opt/kobas*/sqlite3 &&
wget http://kobas.cbi.pku.edu.cn/download/sqlite3/$1.db.gz &&
gunzip $1.db.gz 


