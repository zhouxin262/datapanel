#!/bin/bash
/data/mysql/bin/mysqldump -uroot datapanel > ./db.dmp
tar -czvf db.tar.gz db$(date + %Y%m%d).dmp
rm -f db.dmp