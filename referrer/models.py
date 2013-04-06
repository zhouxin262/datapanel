#coding=utf-8
from django.db import models

'''重复'''
'''delete from referrer_keyword where id in (select id from (select max(id) id, count(*) c from referrer_keyword group by name) t where t.c>1);'''
'''delete from referrer_site where id in (select id from (select max(id) id, count(*) c from referrer_site group by name) t where t.c>1);'''

class Site(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'域名', default='')


class Keyword(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'关键词', default='')
