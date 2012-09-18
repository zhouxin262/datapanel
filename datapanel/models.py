#coding=utf-8
from datetime import datetime
from django.db import models

from django.contrib.auth.models import User

class Project(models.Model):
	"""docstring for Project"""
	name = models.CharField(max_length=20, verbose_name=u'项目名称')
	url = models.CharField(max_length=255, verbose_name=u'项目URL')
	dateline = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
	lastview = models.DateTimeField(verbose_name=u'最后访问时间', auto_now=True)
	creator = models.ForeignKey(User, verbose_name=u'创建用户', related_name='create_project')
	participants = models.ManyToManyField(User, verbose_name=u'参与用户', related_name='participate_projects')
	key = models.CharField(max_length=255, verbose_name=u'', default='')
	token = models.CharField(max_length=255, verbose_name=u'', default='')

	class Meta:
		unique_together = (('name', 'creator'),)
		ordering = ['-lastview']

class Session(models.Model):
	project = models.ForeignKey(Project, related_name='session')
	sn = models.CharField(unique=True,max_length=40, verbose_name=u'用户会话',default='')
	start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'会话开始时间')
	end_time = models.DateTimeField(auto_now=True, verbose_name=u'会话结束时间')
	user_language = models.CharField(max_length=255, verbose_name=u'客户端语言', default='')
	user_timezone = models.CharField(max_length=255, verbose_name=u'客户端时区', default='')
	user_agent = models.CharField(max_length=255, verbose_name=u'客户端类型', default='')
	user_referer = models.CharField(max_length=255, verbose_name=u'客户端来源', default='')
	ipaddress = models.IPAddressField(verbose_name=u'IP地址',null=False,default='0.0.0.0')
#
#class Action(models.Model):
#	project = models.ForeignKey(Project, related_name='action')
#	name = models.CharField(max_length=255, verbose_name=u'动作')
#	url = models.CharField(max_length=255, verbose_name=u'url')
#	xpath = models.CharField(max_length=255, verbose_name=u'dom')
#	event = models.CharField(max_length=255, verbose_name=u'event')

class Track(models.Model):
	session = models.ForeignKey(Session, related_name='track', verbose_name=u'用户会话')
	action = models.CharField( max_length=255,verbose_name=u'事件',default='')
	url = models.CharField(max_length=255, verbose_name=u'url', default='')
	xpath = models.CharField(max_length=255, verbose_name=u'dom', default='')
	event = models.CharField(max_length=255, verbose_name=u'event', default='')
	param = models.CharField(max_length=255, verbose_name=u'参数', default='')
	mark = models.SmallIntegerField(max_length=2, verbose_name=u'统计参数',null = True, default='')
	step = models.IntegerField(max_length=50,null = True,default='')
	dateline = models.DateTimeField(auto_now_add=True)
	timelength = models.IntegerField(max_length=50,null = True,default='')

class TrackGroup(models.Model):
	TYPE_CHOICES = (('U', u'url'), ('A', u'action',))
	DATA_CHOICES = (('C', u'页面点击数'), ('D', u'页面停留时间',))
	CATE_CHOICES = (('A', u'所有页面'), ('L', u'着陆页',), ('F', u'第一次点击',), ('J', u'跳出页',))
	DATE_CHOICES = (('H', u'小时'), ('D', u'天',), ('W', u'周 ',), ('M', u'月',), ('Y', u'年',))
	grouptype = models.CharField(u'统计类型', max_length=1, null=True,blank = False, choices=TYPE_CHOICES)
	groupcate = models.CharField(u'统计分类', max_length=1, null=True,blank = False, choices=CATE_CHOICES)
	groupdate = models.CharField(u'时间类型', max_length=1, null=True,blank = False, choices=DATE_CHOICES)
	datatype = models.CharField(u'数据类型', max_length=1, null=True,blank = False, choices=DATA_CHOICES)
	name = models.CharField(max_length=255, verbose_name=u'Action/url值', default='')
	count = models.IntegerField(u'统计数值', null=True)
	dateline = models.DateTimeField(auto_now_add = False)