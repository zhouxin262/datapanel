#coding=utf-8
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

    def __unicode__(self):
        return self.name

    def add_action(self, name, url):
        a = Action.objects.get_or_create(project=self, name=name)
        if a[1]:
            a[0].url = url
            a[0].save()
        return a[0]


class Action(models.Model):
    """
    Websites' managers defined their own actions
    """
    IS_FLAG_CHOICES = (('Y', '是'), ('N', '否'))
    project = models.ForeignKey(Project, related_name='action')
    name = models.CharField(max_length=255, verbose_name=u'行为名称')
    url = models.CharField(max_length=255, verbose_name=u'URL正则', null=True, blank=True)
    xpath = models.CharField(max_length=255, verbose_name=u'控件', null=True, blank=True)
    event = models.CharField(max_length=255, verbose_name=u'事件', null=True, blank=True)
    is_flag = models.CharField(max_length=1, verbose_name=u'是否是成功标识', null=False, blank=False, default='N', choices=IS_FLAG_CHOICES)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'project'),)


class Keyword(models.Model):
    """
    Websites' manager focus their keyword
    """
    project = models.ForeignKey(Project, related_name='keywords')
    name = models.CharField(max_length=20, verbose_name='关键词')

    class Meta:
        unique_together = (('project', 'name'))
