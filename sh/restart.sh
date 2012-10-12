#!/bin/sh
killall -9 uwsgi
find /home/hongyuan/website_django/datapanel/ -name "*.pyc" -delete
uwsgi -x /home/hongyuan/website_django/datapanel/sh/django.xml
python ./manage.py cleanup
python ./manage.py collectstatic << EOFDJANGO
yes
EOFDJANGO