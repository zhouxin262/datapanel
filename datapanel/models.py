# coding=utf8
from django.db import models


class Timeline(models.Model):
    """
    Group Time Foreign Key
    """
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)

    def get_range(self):
        from datetime import timedelta
        drange = [self.dateline, self.dateline]
        if self.datetype == 'hour':
            drange[1] += timedelta(seconds=3600)
        elif self.datetype == 'day':
            drange[1] += timedelta(seconds=3600 * 24)
        elif self.datetype == 'week':
            drange[1] += timedelta(seconds=3600 * 24 * 7)
        elif self.datetype == 'month':
            drange[1] += timedelta(months=1)
        return drange

    def has_time(self, time):
        drange = self.get_range()
        if time <= drange[1] and time >= drange[0]:
            return True
        return False

    class Meta:
        unique_together = (('datetype', 'dateline'))
