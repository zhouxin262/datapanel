#!/bin/bash
/data/mysql/bin/mysql << EOFMYSQL
drop database datapanel;
create database datapanel charset=utf8;
EOFMYSQL
echo "drop db finished"
python ../manage.py syncdb