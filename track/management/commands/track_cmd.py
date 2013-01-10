#coding=utf-8
from datetime import datetime, timedelta

from django.core.management.base import LabelCommand
from django.db.models import Count, Sum, Avg

from project.models import Project
from track.models import Track, GAction, GReferrerSiteAndAction, GReferrerKeywordAndAction
from datapanel.utils import Group

"""
A management command for statistics
"""


class Command(LabelCommand):
    help = "byaction"
    command_name = "track_cmd"
    label = ""

    def handle_label(self, label, **options):
        print '====started at %s====' % datetime.now()

        days_before = 0
        try:
            days_before = int(label)
        except:
            print 'wrong label, should be int'
            return None

        processing_day = datetime.now() - timedelta(days=days_before + 1)
        print '====processing %s====' % processing_day.strftime("%Y-%m-%d")

        """
        group by time per hour
        """
        print '====processing by hour===='
        for i in range(24):
            # get time range
            s = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
            e = s + timedelta(seconds=3600)
            dateline = s

            # foreach project
            for p in Project.objects.filter():
                # group by track action
                g = Group(Track, GAction)
                g.static_attr = {'project': p, 'timeline__dateline': dateline, 'timeline__datetype': 'hour'}
                g.values = ['action', ]
                g.dynamic_attr = {'action_id': 'action'}
                g.annotate = {'count': Count('action'), 'timelength': Avg('timelength')}
                g.fargs = {'dateline__range': [s, e], 'project': p}
                g.easy_group()

        """
        group by time per day
        """
        # all day data
        s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
        e = s + timedelta(days=1)
        dateline = s

        # foreach projects
        print '====processing by day===='
        for p in Project.objects.filter():
            # group by track action

            g = Group(GAction, GAction)
            g.static_attr = {'project': p, 'timeline__dateline': dateline, 'timeline__datetype': 'day'}
            g.values = ['action', ]
            g.dynamic_attr = {'action_id': 'action'}
            g.annotate = {'count': Sum('count'), 'timelength': Avg('timelength')}
            g.fargs = {'timeline__dateline__range': [s, e], 'project': p}
            g.easy_group()

            # # group by track value
            # g = Group(TrackValue, GValue)
            # g.static_attr = {'project': p, 'dateline': dateline, 'datetype': 'day'}
            # g.values = ['valuetype_id', 'value']
            # g.annotate = {'count': Count('value'), 'timelength': Avg('track__timelength')}
            # g.fargs = {'track__dateline__range': [s, e], 'track__project': p}
            # g.easy_group()

            # group by track action and time and sessionreferrersite
            g = Group(Track, GReferrerSiteAndAction)
            g.static_attr = {'project': p, 'timeline__dateline': dateline, 'timeline__datetype': 'day'}
            g.values = ['action', 'session__referrer_site__id']
            g.dynamic_attr = {'action_id': 'action', 'referrer_site_id': 'session__referrer_site__id'}
            g.annotate = {'count': Count('action'), 'timelength': Avg('timelength')}
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.easy_group()

            # group by track action and time and sessionreferrerkeyword
            g = Group(Track, GReferrerKeywordAndAction)
            g.static_attr = {'project': p, 'timeline__dateline': dateline, 'timeline__datetype': 'day'}
            g.values = ['action', 'session__referrer_keyword__id']
            g.dynamic_attr = {'action_id': 'action', 'referrer_keyword_id': 'session__referrer_keyword__id'}
            g.annotate = {'count': Count('action'), 'timelength': Avg('timelength')}
            g.fargs = {'dateline__range': [s, e], 'project': p}
            g.easy_group()

        print '====moving data===='
        import MySQLdb as mdb
        con = mdb.connect('localhost', 'root', '', 'datapanel')
        cur = con.cursor()
        sql = "SELECT id FROM track_track WHERE dateline<='%s' ORDER BY dateline desc LIMIT 1" % processing_day
        cur.execute(sql)
        last_track_id = cur.fetchone()[0]
        sql = "INSERT INTO %s(id, project_id, session_id, action_id, url, from_track_id, referrer_site_id, referrer_keyword_id, step, timelength, dateline) SELECT id, project_id, session_id, action_id, url, from_track_id, referrer_site_id, referrer_keyword_id, step, timelength, dateline FROM %s f WHERE f.id <= %d" % ('track_trackarch', 'track_track', last_track_id)
        cur.execute(sql)
        sql = "DELETE FROM %s WHERE id <= %d" % ('track_track', last_track_id)
        cur.execute(sql)
        sql = "INSERT INTO %s(id, track_id, valuetype_id, value) SELECT id, track_id, valuetype_id, value FROM %s f WHERE f.track_id <= %d" % ('track_trackvaluearch', 'track_trackvalue', last_track_id)
        cur.execute(sql)
        sql = "DELETE FROM %s WHERE track_id <= %d" % ('track_trackvalue', last_track_id)
        cur.execute(sql)
        sql = "OPTIMIZE TABLE %s" % 'track_track'
        cur.execute(sql)
        sql = "OPTIMIZE TABLE %s" % 'track_trackvalue'
        cur.execute(sql)
        sql = "flush tables"
        cur.execute(sql)
        print '====finished at %s====' % datetime.now()
