#coding=utf-8
from datetime import datetime, timedelta

from django.db.models import Count, Sum, Avg
from django.core.management.base import LabelCommand

from project.models import Project
from session.models import GTime, Session, GReferrerKeyword, GReferrerSite
from datapanel.utils import Group


class Command(LabelCommand):

    def handle_label(self, label, **options):
        days_before = 0
        try:
            days_before = int(label)
        except:
            print 'wrong label, should be int'
            return None

        _s = datetime.now()

        """
        group by time per hour
        """
        for i in range(24):
            used_time = (datetime.now() - _s).seconds
            if used_time > 0:
                print used_time, 'seconds used', '%d seconds left' % (float(23 - i) / (float(i) / used_time))

            # print i,

            # get time range
            s = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
            e = s + timedelta(seconds=3600)
            dateline = s

            # foreach project
            for p in Project.objects.filter():
                # group by time
                g = Group(Session, GTime)
                g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                g.annotate = {'count': Count('id'), 'track_count': Avg('track_count'), 'timelength': Avg('timelength')}
                g.fargs = {'start_time__range': [s, e], 'project': p, 'track_count__gte': 1}
                g.easy_group()
        """
        group by time per day
        """
        # all day data
        s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
        e = s + timedelta(days=1)

        # foreach projects
        for p in Project.objects.filter():
            # group by time
            g = Group(GTime, GTime)
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.annotate = {'count': Sum('count'), 'track_count': Avg('track_count'), 'timelength': Avg('timelength')}
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.easy_group()

            # group by user_referrer_site and time
            g = Group(Session, GReferrerSite)
            g.fargs = {'start_time__range': [s, e], 'project': p, 'track_count__gte': 1}
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.values = ['referrer_site', ]
            g.dynamic_attr = {'referrer_site_id': 'referrer_site'}
            g.annotate = {'count': Count('referrer_site'), 'track_count': Avg('track_count'), 'timelength': Avg('timelength')}
            g.easy_group()

            # group by user_referrer_keyword and time
            g = Group(Session, GReferrerKeyword)
            g.fargs = {'start_time__range': [s, e], 'project': p, 'track_count__gte': 1}
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.values = ['referrer_keyword', ]
            g.dynamic_attr = {'referrer_keyword_id': 'referrer_keyword'}
            g.annotate = {'count': Count('referrer_keyword'), 'track_count': Avg('track_count'), 'timelength': Avg('timelength')}
            g.easy_group()

        print label, '====finished====', datetime.now()
