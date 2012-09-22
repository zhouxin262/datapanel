#coding=utf-8
import datetime

from django.core.management.base import NoArgsCommand

from datapanel.models import Track, TrackGroup
from datapanel.common import tongji,dealdata

"""
A management command for statistics
"""
class Command(NoArgsCommand):
    help = "tj"

    def handle_noargs(self, **options):
        dealdata()
        tg = TrackGroup.objects.filter().values('dateline').order_by('-dateline')
        if tg:
            starttime = tg[0]['dateline']
        else:
            t = Track.objects.filter().values('dateline').order_by('dateline')
            if t:
                starttime = t[0]['dateline']
            else:
                return False

        raw_starttime = starttime
        for grouptype in ('U','A'):
            for datatype in ('C','D'):
                for groupcate in ('A','L','F','J'):
                    #for groupdate in ('H','D','W','M','Y'):
                    starttime = None

                    groupdate = 'H'
                    starttime = raw_starttime.replace(minute=0, second=0, microsecond=0)
                    delta = datetime.datetime.now() - starttime
                    for i in range((delta.days*3600*24+delta.seconds)/3600):
                        endtime = starttime + datetime.timedelta(hours=1)
                        tongji(starttime, endtime, grouptype, datatype, groupcate, groupdate)
                        starttime = starttime + datetime.timedelta(hours=1)

                    groupdate = 'D'
                    starttime = raw_starttime.replace(hour=0, minute=0, second=0, microsecond=0)
                    delta = datetime.datetime.now() - starttime
                    for i in range(delta.days):
                        endtime = starttime + datetime.timedelta(days=1)
                        tongji(starttime, endtime, grouptype, datatype, groupcate, groupdate)
                        starttime = starttime + datetime.timedelta(days=1)

                    groupdate = 'W'
                    starttime = raw_starttime.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=raw_starttime.weekday())
                    delta = datetime.datetime.now() - starttime
                    for i in range((delta.days/7)):
                        endtime = starttime + datetime.timedelta(days=7)
                        tongji(starttime, endtime, grouptype, datatype, groupcate, groupdate)
                        starttime = starttime + datetime.timedelta(days=7)

                    groupdate = 'M'
                    starttime = raw_starttime.replace(day=1, minute=0, second=0, microsecond=0)
                    delta = (datetime.datetime.now().year - starttime.year) * 12 + (datetime.datetime.now().month - starttime.month)
                    for i in range((delta)):
                        endtime = starttime.replace(month=starttime.month+1, day=1, minute=0, second=0, microsecond=0)
                        tongji(starttime, endtime, grouptype, datatype, groupcate, groupdate)
                        starttime = starttime.replace(month=starttime.month+1, day=1, minute=0, second=0, microsecond=0)

