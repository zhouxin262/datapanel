#coding=utf-8
from django.db import models

from project.models import Project, Action
from session.models import Session
from track.models import Track


class Funnel(models.Model):
    project = models.ForeignKey(Project, related_name='funnel')
    name = models.CharField(u'命名', max_length=20)


class FunnelAction(models.Model):
    funnel = models.ForeignKey(Funnel, related_name='action')
    order = models.IntegerField()
    action = models.ForeignKey(Action, related_name='funnelaction')
