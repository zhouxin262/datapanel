#!/bin/bash
/data/mysql/bin/mysql datapanel << EOFMYSQL
truncate table datapanel_session;
truncate table datapanel_track;
truncate table datapanel_trackgroup;
EOFMYSQL
echo "finished"