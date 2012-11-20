#coding=utf-8
from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'域名', default='')


class Keyword(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'关键词', default='')
