#!/bin/sh
sudo killall -9 uwsgi
find /home/hongyuan/website_django/datapanel/ -name "*.pyc" -delete
uwsgi -x /home/hongyuan/website_django/datapanel/django.xml