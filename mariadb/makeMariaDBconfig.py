#!/usr/bin/python
# makeMariaDBconfig.py
# version 1.0
# Kai Yu
# github.com/readline
# 150515
##############################################

template = '''#!/bin/bash

__mysql_config() {
# Hack to get MySQL up and running... I need to look into it more.
echo "Running the mysql_config function."
mysql_install_db
chown -R mysql:mysql /var/lib/mysql
/usr/bin/mysqld_safe & 
sleep 10
}

__start_mysql() {
echo "Running the start_mysql function."
mysqladmin -u root password mysqlPassword
{{SQL TO ADD}}
killall mysqld
sleep 10
}

# Call all functions
__mysql_config
__start_mysql
'''

def getConfig():
    infile = open('MariaDB.conf', 'r')
    tmp = {}
    while 1:
        line = infile.readline()
        if not line: break
        if line == '\n' or line[0] == '#': continue
        c = line.rstrip().split('\t')
        tmp[c[0]] = c[1]
    infile.close()
    return tmp

def main(template):
    conf = getConfig()
    tmp = template.replace('root', conf['username'])
    tmp = tmp.replace('mysqlPassword', conf['password'])
    if conf['sqlfile'] == 'NA':
        sql = '''
mysql -uroot -pmysqlPassword -e "CREATE DATABASE testdb"
mysql -uroot -pmysqlPassword -e "GRANT ALL PRIVILEGES ON testdb.* TO 'testdb'@'localhost' IDENTIFIED BY 'mysqlPassword'; FLUSH PRIVILEGES;"
mysql -uroot -pmysqlPassword -e "GRANT ALL PRIVILEGES ON *.* TO 'TemplateDBname'@'%' IDENTIFIED BY 'mysqlPassword' WITH GRANT OPTION; FLUSH PRIVILEGES;"
mysql -uroot -pmysqlPassword -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'mysqlPassword' WITH GRANT OPTION; FLUSH PRIVILEGES;"
mysql -uroot -pmysqlPassword -e "select user, host FROM mysql.user;"
'''
        sql = sql.replace('root', conf['username'])
        sql = sql.replace('mysqlPassword', conf['password'])
        sql = sql.replace('TemplateDBname', conf['dbname'])
        sql = sql.replace('testdb', conf['dbname'])
        template = tmp.replace('{{SQL TO ADD}}', sql)
    else:
        tmp = template.replace('root', conf['username'])
        tmp = tmp.replace('mysqlPassword', conf['password'])
        sql = 'mysql -u%s -p%s %s < %s\n' %(conf['username'],
                                            conf['password'],
                                            conf['dbname'],
                                            conf['sqlfile'])
        template = tmp.replace('{{SQL TO ADD}}', sql)
    savefile = open('MariaDB.init.sh', 'w')
    savefile.write(template)
    savefile.close()
    print 'MariaDB init script have wrote in MariaDB.init.sh'
    if conf['sqlfile'] == 'NA':
        print 'Empty database %s would be created.' %conf['dbname']
    else:
        print 'Database %s would be created from SQL file %s.' \
              %(conf['dbname'], conf['sqlfile'])

if __name__ == '__main__':
    main(template)
