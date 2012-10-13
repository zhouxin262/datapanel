#coding=utf-8
import ast, urlparse
from datetime import datetime, timedelta, tzinfo
from django.db import models
from django.contrib.auth.models import User
from datapanel.utils import smart_decode

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

    def first_track(self):
        try:
            return self.track.filter().order_by('dateline')[0]
        except IndexError:
            return None

    def last_track(self):
        try:
            return self.track.filter().order_by('-dateline')[0]
        except IndexError:
            return None
#
#class Action(models.Model):
#    project = models.ForeignKey(Project, related_name='action')
#    name = models.CharField(max_length=255, verbose_name=u'动作')
#    url = models.CharField(max_length=255, verbose_name=u'url')
#    xpath = models.CharField(max_length=255, verbose_name=u'dom')
#    event = models.CharField(max_length=255, verbose_name=u'event')

class Track(models.Model):
    """
    User behavior action track
    """
    session = models.ForeignKey(Session, related_name='track', verbose_name=u'用户会话')
    action = models.CharField( max_length=255,verbose_name=u'事件',default='')
    url = models.CharField(max_length=255, verbose_name=u'url', default='')
    xpath = models.CharField(max_length=255, verbose_name=u'dom', default='')
    event = models.CharField(max_length=255, verbose_name=u'event', default='')
    param = models.CharField(max_length=255, verbose_name=u'参数', default='')
    # mark = models.SmallIntegerField(max_length=2, verbose_name=u'统计参数', null=False, default=0)
    # is_landing = models.SmallIntegerField(max_length=1, verbose_name=u'是否landing', null=False, default=0)
    # step = models.IntegerField(max_length=50,null=False,default=0)
    # timelength = models.IntegerField(max_length=50, null=False, default=0)
    dateline = models.DateTimeField(auto_now_add=True)
    hourline = models.DateTimeField(auto_now_add=False, verbose_name=u"小时")
    dayline = models.DateTimeField(auto_now_add=False, verbose_name=u"天")
    weekline = models.DateTimeField(auto_now_add=False, verbose_name=u"周")
    monthline = models.DateTimeField(auto_now_add=False, verbose_name=u"月")

    def action_display(self):
        return smart_decode(slef.action).encode('utf-8')

    def set_times(self, save=False):
        if self.dateline:
            self.hourline = self.dateline.replace(minute=0, second=0, microsecond=0)
            self.dayline = self.dateline.replace(hour=0, minute=0, second=0, microsecond=0)
            self.weekline = self.dateline.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=self.dateline.weekday())
            self.monthline = self.dateline.replace(day=1, minute=0, second=0, microsecond=0)
            if save:
                self.save()
            else:
                return True
        else:
            return False

    def param_display(self):
        try:
            param = ast.literal_eval(self.param)
            if param.has_key('referer'):
                parsed_url = urlparse.urlparse(param['referer'])
                if parsed_url.netloc:
                    param['referer_site'] = parsed_url.netloc
                    param['referer_parsed'] = True
                    querystring = urlparse.parse_qs(parsed_url.query,True)
                    if parsed_url.netloc.find('baidu')!=-1:
                        #baidu
                        if querystring.has_key('wd'):
                            param['referer_keyword'] = smart_decode(querystring['wd'][0])
                        elif querystring.has_key('word'):
                            param['referer_keyword'] = smart_decode(querystring['word'][0])
                    if parsed_url.netloc.find('sougou')!=-1:
                        #sougou
                        if querystring.has_key('query'):
                            param['referer_keyword'] = smart_decode(querystring['query'][0])
            return param
        except:
            return None

# class TrackGroup(models.Model):
#     TYPE_CHOICES = (('U', u'url'), ('A', u'action',))
#     DATA_CHOICES = (('C', u'页面点击数'), ('D', u'页面停留时间',))
#     CATE_CHOICES = (('A', u'所有页面'), ('L', u'着陆页',), ('F', u'第一次点击',), ('J', u'跳出页',))
#     DATE_CHOICES = (('H', u'小时'), ('D', u'天',), ('W', u'周 ',), ('M', u'月',), ('Y', u'年',))
#     project = models.ForeignKey(Project, related_name='trackgroup')
#     grouptype = models.CharField(u'统计类型', max_length=1, null=True,blank = False, choices=TYPE_CHOICES)
#     groupcate = models.CharField(u'统计分类', max_length=1, null=True,blank = False, choices=CATE_CHOICES)
#     groupdate = models.CharField(u'时间类型', max_length=1, null=True,blank = False, choices=DATE_CHOICES)
#     datatype = models.CharField(u'数据类型', max_length=1, null=True,blank = False, choices=DATA_CHOICES)
#     name = models.CharField(max_length=255, verbose_name=u'Action/url值', default='')
#     count = models.IntegerField(u'统计数值', null=True)
#     dateline = models.DateTimeField(auto_now_add = False)

class Referer(models.Model):
    session = models.ForeignKey(Session, related_name='referer', verbose_name=u'用户会话')
    site = models.CharField(max_length=255, verbose_name=u'site', default='')
    keyword = models.CharField(max_length=255, verbose_name=u'keyword', default='')
    url = models.CharField(max_length=255, verbose_name=u'url ', default='')