#coding=utf-8
from django.db import models

from project.models import Project
from project.models import Action


class Funnel(models.Model):
    project = models.ForeignKey(Project, related_name='funnel')
    name = models.CharField(u'命名', max_length=20)


class FunnelAction(models.Model):
    funnel = models.ForeignKey(Funnel, related_name='action')
    order = models.IntegerField()
    action = models.ForeignKey(Action, related_name='funnelaction')

class Swipe(models.Model):
    project = models.ForeignKey(Funnel, related_name='swipes')
    from_action = models.ForeignKey(Action, related_name='swipe_from')
    to_action = models.ForeignKey(Action, related_name='swipe_to')

