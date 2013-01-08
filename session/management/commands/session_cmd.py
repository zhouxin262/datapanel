#coding=utf-8
import time
from datetime import datetime, timedelta

from django.db.models import Count, Sum, Avg
from django.core.management.base import LabelCommand

from project.models import Project
from session.models import GTime, Session, GReferrerKeyword, GReferrerSite
from datapanel.utils import Group


class Command(LabelCommand):

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
        print '====processing by day===='
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

        print '====moving data===='
        import MySQLdb as mdb
        con = mdb.connect('localhost', 'root', '', 'datapanel')
        cur = con.cursor()
        sql = "SELECT id FROM session_session WHERE start_time<='%s' ORDER BY start_time desc LIMIT 1" % processing_day
        cur.execute(sql)
        last_id = cur.fetchone()[0]
        sql = "INSERT INTO %s(id, project_id, session_key, permanent_session_key, start_time, end_time, user_language, user_timezone, agent_id, os_id, device_id, referrer_site_id, referrer_keyword_id, track_count, timelength, ipaddress) SELECT id, project_id, session_key, permanent_session_key, start_time, end_time, user_language, user_timezone, agent_id, os_id, device_id, referrer_site_id, referrer_keyword_id, track_count, timelength, ipaddress FROM %s f WHERE f.id <= %d" % ('session_sessionarch', 'session_session', last_id)
        cur.execute(sql)
        sql = "DELETE FROM %s WHERE id <= %d" % ('session_session', last_id)
        cur.execute(sql)
        sql = "INSERT INTO %s(id, session_id, valuetype_id, value) SELECT id, session_id, valuetype_id, value FROM %s f WHERE f.session_id <= %d" % ('session_sessionvaluearch', 'session_sessionvalue', last_id)
        cur.execute(sql)
        sql = "DELETE FROM %s WHERE session_id <= %d" % ('session_sessionvalue', last_id)
        cur.execute(sql)
        print '====finished at %s====' % datetime.now()
