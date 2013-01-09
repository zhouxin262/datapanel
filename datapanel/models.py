#coding=utf8
from django.db import models

class Timeline(models.Model):
    """
    Group Time Foreign Key
    """
    datetype = models.CharField(u'统计类型',null=True, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)

    class Meta:
        unique_together = (('datetype', 'dateline'))
