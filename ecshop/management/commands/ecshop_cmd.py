#coding=utf-8
from datetime import datetime, timedelta

from django.core.management.base import LabelCommand
from django.db.models import Sum, Count
from django.core.cache import cache

from session.models import Session
from project.models import Project
from track.models import Track, TrackValue
from ecshop.models import Report1, OrderGoods, OrderInfo, Report2, Goods
from datapanel.models import Timeline
from datapanel.utils import Group


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
            timeline = Timeline.objects.get_or_create(datetype='day', dateline=s)
            try:
                r = Report1.objects.get(timeline=timeline[0])
            except Report1.DoesNotExist:
                r = Report1()

            r.project = p
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

            def get_goods(datarow):
                goods = Goods.objects.get_or_create(project=p, goods_id=datarow['value'])
                return goods[0]

            # group by track value
            g = Group(TrackValue, Report2)
            g.static_attr = {'project': p, 'timeline': timeline[0]}
            g.values = ['value']
            g.annotate = {'viewcount': Count('value')}
            g.fargs = {'track__dateline__range': [s, e], 'track__project': p, 'valuetype__name': 'goods_goods_id'}
            g.function_attr = {'goods': get_goods}
            g.easy_group()

            def get_goods2(datarow):
                goods = Goods.objects.get_or_create(project=p, goods_id=datarow['goods_id'])
                return goods[0]

            g = Group(OrderGoods, Report2)
            g.static_attr = {'project': p, 'timeline': timeline[0]}
            g.values = ['goods_id']
            g.exclude_attr = ['goods_id']
            g.annotate = {'sellcount': Sum('goods_number')}
            g.fargs = {'order__dateline__range': [s, e], 'project': p}
            g.function_attr = {'goods': get_goods2}
            g.easy_group(update=True)
        cache.clear()
        print label, '====finished====', datetime.now()
