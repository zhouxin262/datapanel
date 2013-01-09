#coding=utf-8
from datetime import datetime, timedelta

from django.core.management.base import LabelCommand
from django.db.models import Sum, Count

from session.models import Session
from project.models import Project
from track.models import Track, TrackValue
from ecshop.models import Report1, OrderGoods, OrderInfo
from datapanel.models import Timeline


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

        # import MySQLdb as mdb
        # con = mdb.connect('localhost', 'root', '', 'datapanel')
        # cur = con.cursor()
        # foreach projects
        for p in Project.objects.filter():
            r = Report1()
            r.project = p

            timeline = Timeline.objects.get_or_create(datetype = 'day', dateline = s)
            r.timeline = timeline[0]

            r.userview = Session.objects.filter(project=p, end_time__range=[s, e]).values('ipaddress').distinct().count()
            r.pageview = Track.objects.filter(session__project=p, dateline__range=[s, e]).count()
            r.goodsview = TrackValue.objects.filter(track__session__project=p, valuetype__name='goods_goods_id', track__dateline__range=[s, e]).values('value').distinct().count()
            r.goodspageview = Track.objects.filter(session__project=p, dateline__range=[s, e], action__name='goods').count()

            orderinfo = OrderInfo.objects.filter(project=p, dateline__range=[s, e]).aggregate(c=Count('id'), s=Sum('order_amount'))
            r.ordercount = orderinfo['c']
            r.ordergoodscount = OrderGoods.objects.filter(project=p, order__dateline__range=[s, e]).aggregate(Sum('goods_number'))['goods_number__sum']
            r.orderamount = orderinfo['s']
            r.save()
        print label, '====finished====', datetime.now()
