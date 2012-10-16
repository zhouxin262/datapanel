#coding=utf-8
from datetime import tzinfo, timedelta, datetime

from django.core.management.base import NoArgsCommand
from django.db.models import Count

from datapanel.models import Track, TrackGroup, Project
from datapanel.utils import UTC

"""
A management command for statistics
"""
class Command(NoArgsCommand):
    help = "tj"

    def handle_noargs(self, **options):
        # deal with those data by projects
        for p in Project.objects.filter():
            # get the last updated hourline
            try:
                last_updated_hourline = TrackGroup.objects.filter().order_by('dateline')[0]
            except IndexError:
                last_updated_hourline = p.dateline
            # start statistics
            args = {'session__project': p, 'hourline__gt': last_updated_hourline}
            ts = Track.objects.filter(**args).values('action', 'hourline').annotate(c = Count('id'))
            print last_updated_hourline
            for t in ts:
                print t
