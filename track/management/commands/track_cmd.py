#coding=utf-8
from datetime import datetime, timedelta

from django.core.management.base import LabelCommand
from django.db.models import Count, Sum

from project.models import Project
from track.models import Track, TrackValue, GAction, GValue, GReferrerSiteAndAction, GReferrerKeywordAndAction
from datapanel.utils import Group

"""
A management command for statistics
"""


class Command(LabelCommand):
    help = "byaction"
    command_name = "track_cmd"
    label = ""

    def handle_label(self, label, **options):
        print label, '====started====', datetime.now()

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

            print i,

            # get time range
            s = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
            e = s + timedelta(seconds=3600)
            dateline = s

            # foreach project
            for p in Project.objects.filter():
                # # group by track action
                # g = Group(Track, GAction)
                # g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                # g.values = ['action', ]
                # g.dynamic_attr = {'action_id': 'action'}
                # g.annotate = {'count': Count('action'), 'timelength': Sum('timelength')}
                # g.fargs = {'dateline__range': [s, e], 'project': p}
                # g.easy_group()

                # # group by track value
                # g = Group(TrackValue, GValue)
                # g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                # g.values = ['name', 'value']
                # g.annotate = {'count': Count('value'), 'timelength': Sum('track__timelength')}
                # g.fargs = {'track__dateline__range': [s, e], 'track__project': p}
                # g.eargs = {'where': ["name not like 'referrer%%' and length(value) < 30"], 'params': []}
                # g.easy_group()

                # group by track action and time and sessionreferrersite

                # get actions that need to calc
                g = Group(Track, GReferrerSiteAndAction)
                g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                g.values = ['action', 'session__user_referrer_site']
                g.dynamic_attr = {'action_id': 'action', 'value': 'session__user_referrer_site'}
                g.annotate = {'count': Count('action'), 'timelength': Sum('timelength')}
                g.fargs = {'dateline__range': [s, e], 'project': p}
                g.exargs = {"session__user_referrer_site": ""}
                g.easy_group()

                # group by track action and time and sessionreferrerkeyword
                g = Group(Track, GReferrerKeywordAndAction)
                g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'hour'}
                g.values = ['action', 'session__user_referrer_keyword']
                g.dynamic_attr = {'action_id': 'action', 'value': 'session__user_referrer_keyword'}
                g.annotate = {'count': Count('action'), 'timelength': Sum('timelength')}
                g.fargs = {'dateline__range': [s, e], 'project': p}
                g.exargs = {"session__user_referrer_keyword": ""}
                g.easy_group()

        """
        group by time per day
        """
        # all day data
        s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
        e = s + timedelta(days=1)
        dateline = s

        # foreach projects
        for p in Project.objects.filter():
            # group by track action

            # g = Group(GAction, GAction)
            # g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            # g.values = ['action', ]
            # g.dynamic_attr = {'action_id': 'action'}
            # g.annotate = {'count': Sum('count'), 'timelength': Sum('timelength')}
            # g.fargs = {'dateline__range': [s, e], 'project': p}
            # g.easy_group()

            # g = Group(GValue, GValue)
            # g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            # g.values = ['name', 'value']
            # g.annotate = {'count': Sum('count'), 'timelength': Sum('timelength')}
            # g.fargs = {'dateline__range': [s, e], 'project': p}
            # g.easy_group()

            g = Group(GReferrerSiteAndAction, GReferrerSiteAndAction)
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.values = ['action', 'value']
            g.dynamic_attr = {'action_id': 'action'}
            g.annotate = {'count': Sum('count'), 'timelength': Sum('timelength')}
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.easy_group()

            g = Group(GReferrerKeywordAndAction, GReferrerKeywordAndAction)
            g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            g.values = ['action', 'value']
            g.dynamic_attr = {'action_id': 'action'}
            g.annotate = {'count': Sum('count'), 'timelength': Sum('timelength')}
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.easy_group()

        print label, '====finished====', datetime.now()
