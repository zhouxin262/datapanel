#coding=utf-8
import time
from datetime import tzinfo, timedelta, datetime

from django.core.management.base import NoArgsCommand
from django.db.models import Count

from datapanel.models import Track, Project, TrackGroupByClick
from datapanel.utils import UTC

"""
A management command for statistics
"""
class Command(NoArgsCommand):
    help = "tj"

    def handle_noargs(self, **options):
        # deal with those data by projects
        for p in Project.objects.filter():
            # get the last updated time
            for datetype in ['hourline', 'dayline', 'weekline', 'monthline']:
                try:
                    last_updated_hourline = TrackGroupByClick.objects.filter(datetype = datetype).order_by('-dateline')[0].dateline
                except IndexError:
                    last_updated_hourline = p.dateline
                # start statistics
                print 'deal with track group by:', p.name, datetype, last_updated_hourline
                args = {'session__project': p, datetype + '__gt': last_updated_hourline}
                ts = Track.objects.filter(**args)

                if ts:
                    ts = ts.values('action', datetype).annotate(c = Count('id'))
                    for t in ts:
                        try:
                            trackGroupByClick = TrackGroupByClick.objects.get(project = p, datetype=datetype, action=t['action'], dateline=time.mktime(t[datetype].timetuple()))
                            trackGroupByClick.value = t['c']
                            trackGroupByClick.save()
                        except TrackGroupByClick.DoesNotExist:
                            trackGroupByClick = TrackGroupByClick()
                            trackGroupByClick.project = p
                            trackGroupByClick.datetype = datetype
                            trackGroupByClick.dateline = time.mktime(t[datetype].timetuple())
                            trackGroupByClick.action = t['action']
                            trackGroupByClick.value = t['c']
                            trackGroupByClick.save()