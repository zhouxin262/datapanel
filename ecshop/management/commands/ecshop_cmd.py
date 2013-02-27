# coding=utf-8
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
        s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before)
        e = s + timedelta(days=1)

        for p in Project.objects.filter():
            timeline = Timeline.objects.get_or_create(datetype='day', dateline=s)
            Report1.objects.generate(project=p, timeline=timeline[0], start_dateline=s, end_dateline=e, save=True)

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
