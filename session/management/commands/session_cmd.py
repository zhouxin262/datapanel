#coding=utf-8
import time
from datetime import datetime, timedelta

from django.db.models import Count, Sum
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
                g.annotate = {'count': Count('id'), 'track_count': Sum('track_count')}
                g.fargs = {'start_time__range': [s, e], 'project': p}
                g.easy_group()

                # group by user_referrer_site and time
                g = Group(Session, GReferrerSite)
                g.fargs = {'start_time__range': [s, e], 'project': p}
                g.eargs = {'where': ["user_referrer_site <> ''"]}
                g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                g.values = ['user_referrer_site', ]
                g.annotate = {'count': Count('user_referrer_site'), 'track_count': Sum('track_count')}
                g.easy_group()

                # group by user_referrer_keyword and time
                g = Group(Session, GReferrerKeyword)
                g.fargs = {'start_time__range': [s, e], 'project': p}
                g.eargs = {'where': ["user_referrer_keyword <> ''"]}
                g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                g.values = ['user_referrer_keyword', ]
                g.annotate = {'count': Count('user_referrer_keyword'), 'track_count': Sum('track_count')}
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
            g.annotate = {'count': Sum('count'), 'track_count': Sum('track_count')}
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.easy_group()

            # group by user_referrer_site and time
            g = Group(GReferrerSite, GReferrerSite)
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.values = ['user_referrer_site', ]
            g.annotate = {'count': Sum('count'), 'track_count': Sum('track_count')}
            g.easy_group()

            g = Group(GReferrerKeyword, GReferrerKeyword)
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.values = ['user_referrer_keyword', ]
            g.annotate = {'count': Count('count'), 'track_count': Sum('track_count')}
            g.easy_group()

        print label, '====finished====', datetime.now()
