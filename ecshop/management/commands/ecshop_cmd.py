#coding=utf-8
import time
from datetime import datetime, timedelta

from django.db.models import Count, Sum, Avg
from django.core.management.base import LabelCommand

from project.models import Project
from session.models import Session
from track.models import Track
from ecshop.models import Report1


class Command(LabelCommand):

    def handle_label(self, label, **options):
        print label, '====start====', datetime.now()
        days_before = 0
        try:
            days_before = int(label)
        except:
            print 'wrong label, should be int'
            return None

        """
        group by time per day
        """
        # all day data
        s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
        e = s + timedelta(days=1)

        import MySQLdb as mdb
        con = mdb.connect('localhost', 'root', '', 'datapanel')
        cur = con.cursor()
        # foreach projects
        for p in Project.objects.filter():
            r = Report1()
            r.project = p
            r.datetype = 'day'
            r.dateline = s

            sql = """select count(distinct ipaddress) from session_session where end_time>='%s' and end_time<'%s'""" % (s.isoformat(),  e.isoformat())
            cur.execute(sql)
            r.userview = cur.fetchone()[0]
            r.pageview = Track.objects.filter(session__project=p, dateline__range=[s, e]).count()

            sql = """select count(distinct tv.value) from track_trackvalue tv join track_track t
on tv.track_id = t.id
where valuetype_id='2' and t.dateline>='%s' and t.dateline<'%s'""" % (s.isoformat(), e.isoformat())
            cur.execute(sql)
            r.goodsview = cur.fetchone()[0]
            r.goodspageview = Track.objects.filter(session__project=p, dateline__range=[s, e], action__name='goods').count()
            sql = """select count(*) from ecshop_orderinfo where dateline>='%s' and dateline<'%s'""" % (s.isoformat(), e.isoformat())
            cur.execute(sql)
            r.ordercount = cur.fetchone()[0]
            sql = sql = """select sum(order_amount) from ecshop_orderinfo where dateline>='%s' and dateline<'%s'""" % (s.isoformat(), e.isoformat())
            cur.execute(sql)
            r.orderamount = cur.fetchone()[0]
            r.save()
        print label, '====finished====', datetime.now()
