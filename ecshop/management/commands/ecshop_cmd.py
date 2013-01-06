#coding=utf-8
from datetime import datetime, timedelta

from django.core.management.base import LabelCommand
from django.db.models import Sum, Count

from project.models import Project
from track.models import Track
from ecshop.models import Report1, OrderGoods, OrderInfo


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
            orderinfo = OrderInfo.objects.filter(dateline__range=[s, e]).aggregate(c=Count('id'), s=Sum('order_amount'))
            r.ordercount = orderinfo['c']
            r.ordergoodscount = OrderGoods.objects.filter(order__dateline__range=[s, e]).aggregate(Sum('goods_number'))['goods_number__sum']
            r.orderamount = orderinfo['s']
            r.save()
        print label, '====finished====', datetime.now()
