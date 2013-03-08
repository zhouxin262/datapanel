# coding=utf-8
from datetime import datetime

from django.db import models
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from datapanel.models import Timeline
from project.models import Project
from session.models import Session
from track.models import Track, TrackValue


class OrderManager(models.Manager):
    def process(self, project, order_sn, order_amount=0, goods_list={}, session=None, status=0, *args, **kwargs):
        try:
            order = OrderInfo.objects.get(project=project, order_sn=order_sn)
        except OrderInfo.DoesNotExist:
            order = OrderInfo()
            order.project = project
            if session:
                order.session = session
            order.order_sn = order_sn

        # update order info
        try:
            order_amount = float(order_amount)
            status = int(status)
            if order_amount > 0 and not order.order_amount == order_amount:
                order.order_amount = order_amount
            if status > 0 and not order.order_status == status:
                order.dateline = datetime.now()  # confirm dateline
                order.order_status = status
            order.save()
        except:
            pass

        # update order goods
        if goods_list:
            # remove all
            OrderGoods.objects.filter(project=project, session=session, order=order).delete()
            # create new
            order_goods = []
            for goods_id, goods_number in goods_list.items():
                og = OrderGoods()
                og.project = project
                og.session = session
                og.order = order
                og.goods_id = goods_id
                og.goods_number = goods_number
                order_goods.append(og)
            OrderGoods.objects.bulk_create(order_goods)


class OrderInfo(models.Model):
    STATUS_CHOICES = ((0, u"待确认"), (1, u"已确认"), (2, u"已取消"), (3, u"无效"), (4, u"退货"), (5, u"已发货"), )

    project = models.ForeignKey(Project, related_name='esc_orderinfo')
    session = models.ForeignKey(Session, related_name='esc_orderinfo')
    order_sn = models.CharField(max_length=50, verbose_name=u"订单编号")
    order_amount = models.DecimalField(null=True, max_digits=11, decimal_places=3, default=0)
    dateline = models.DateTimeField(null=True)
    add_dateline = models.DateTimeField(auto_now_add=True, null=True)
    order_status = models.IntegerField(max_length=1, default=0)

    objects = OrderManager()


class OrderGoods(models.Model):
    project = models.ForeignKey(Project, related_name='esc_ordergoods')
    session = models.ForeignKey(Session, related_name='esc_ordergoods')
    order = models.ForeignKey(OrderInfo)
    goods_id = models.IntegerField(null=True, default=0)
    goods_number = models.IntegerField(null=True, default=0)

    def goods(self):
        try:
            return Goods.objects.get(project=self.project, goods_id=self.goods_id)
        except:
            return None


class GoodsManager(models.Manager):
    def process(self, project, goods_id, cat_id=0, goods_name='', goods_price=0, *args, **kwargs):
        g = Goods.objects.get_or_create(project=project, goods_id=goods_id)
        if not (g[0].cat_id == cat_id and g[0].goods_name == goods_name and g[0].goods_price == goods_price):
            g[0].cat_id = cat_id
            g[0].goods_name = goods_name
            g[0].goods_price = goods_price
            g[0].save()


class Goods(models.Model):
    project = models.ForeignKey(Project)
    cat_id = models.IntegerField(null=True, default=0)
    goods_id = models.IntegerField(null=True, default=0)
    goods_name = models.CharField(null=True, default='', max_length=255)
    goods_price = models.DecimalField(null=True, max_digits=11, decimal_places=3, default=0)

    objects = GoodsManager()

    class Meta:
        unique_together = (('project', 'goods_id'))


class Report1Manager(models.Manager):
    def generate(self, project, timeline, save=False):
        try:
            r = Report1.objects.get(project=project, timeline=timeline)
        except Report1.DoesNotExist:
            r = Report1()
            r.project = project
            r.timeline = timeline

        drange = timeline.get_range()
        r.userview = Session.objects.filter(project=project, end_time__range=drange).values('ipaddress').distinct().count()
        r.pageview = Track.objects.filter(session__project=project, dateline__range=drange).count()
        r.goodsview = TrackValue.objects.filter(track__session__project=project, valuetype__name='goods_goods_id',
                                                track__dateline__range=drange).values('value').distinct().count()
        r.goodspageview = Track.objects.filter(session__project=project, dateline__range=drange, action__name='goods').count()
        orderinfo = OrderInfo.objects.filter(
            project=project, dateline__range=drange, order_status__in=[1, 3, 5]).aggregate(c=Count('id'), s=Sum('order_amount'))
        r.ordercount = orderinfo['c']
        r.orderamount = orderinfo['s']
        r.ordergoodscount = OrderGoods.objects.filter(project=project, order__dateline__range=drange, order__order_status__in=[1, 3, 5]
                                                      ).aggregate(Sum('goods_number'))['goods_number__sum']
        r.get_order_set(project)

        if save:
            r.save()
        return r

    def cache(self, project, timeline=None):
        if not timeline:
            s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            timeline = Timeline.objects.get_or_create(datetype='day', dateline=s)[0]

        key = "ecshop.report1|p:" + str(project.id) + "|d:" + timeline.datetype
        value = cache.get(key, {"timeline": None, "data": None})
        in_time = timeline.judge(datetime.now())

        if in_time == 'lt':
            if value['timeline'] and value['data']:
                value['data'].save()
                value = {"timeline": None, "data": None}
        elif in_time == 'gt': 
            return (key, Report1.objects.generate(project, timeline, True)) 

        # check again
        if not value['timeline'] or not  value['data']:
            value = {'timeline': timeline, 'data': Report1.objects.generate(project, timeline)}
            cache.set(key, value)
        return (key, value)


@receiver(post_save)
def report1_receiver(sender, instance, created, **kwargs):
    if hasattr(instance, 'project'):
        if created and sender.__name__ in ('Session', 'Track'):
            (key, value) = Report1.objects.cache(instance.project)
            if sender.__name__ == 'Session':
                value["data"].userview += 1
            elif sender.__name__ == 'Track':
                value["data"].pageview += 1
                if instance.action.name == "goods":
                    value["data"].goodspageview += 1
            cache.set(key, value)

        elif sender.__name__ == 'OrderInfo':
            (key, value) = Report1.objects.cache(instance.project)
            if instance.order_status in [1, 3, 5] and instance.order_sn not in value.order_set and value.timeline.has_time(instance.dateline):
                value["data"].order_set.append(instance.order_sn)
                value["data"].ordercount += 1
                value["data"].orderamount += instance.order_amount
                value["data"].ordergoodscount += instance.ordergoods_set.count()
                cache.set(key, value)


class Report1(models.Model):
    """ overview """
    project = models.ForeignKey(Project, related_name='esc_report1')
    timeline = models.ForeignKey(Timeline, null=True)
    userview = models.IntegerField(u'UV', null=True, default=0)
    pageview = models.IntegerField(u'PV', null=True, default=0)
    goodsview = models.IntegerField(u'访问产品的个数', null=True, default=0)
    goodspageview = models.IntegerField(u'产品页访问数', null=True, default=0)
    ordercount = models.IntegerField(u'订单量', null=True, default=0)
    ordergoodscount = models.IntegerField(u'订单商品件数', null=True, default=0)
    orderamount = models.IntegerField(u'订单总额', null=True, default=0)

    objects = Report1Manager()

    def ip_convert_ratio(self):
        if not self.userview == 0:
            return round(float(self.goodspageview) / float(self.userview), 4) * 100
        else:
            return 0

    def ip_pageview_ratio(self):
        if not self.userview == 0:
            return round(float(self.pageview) / float(self.userview), 4) * 100
        else:
            return 0

    def ip_order_ratio(self):
        if not self.userview == 0:
            return round(float(self.ordercount) / float(self.userview), 5) * 1000
        else:
            return 0

    def get_order_set(self, project):
        self.order_set = [o.order_sn for o in OrderInfo.objects.filter(
            project=project, dateline__range=self.timeline.get_range(), order_status__in=[1, 3, 5])]
        return self.order_set


class Report2(models.Model):
    """
    Goods Report
    including goodsview and goods selling data
    """
    project = models.ForeignKey(Project, related_name='esc_report2')
    timeline = models.ForeignKey(Timeline, null=True)
    goods = models.ForeignKey(Goods, null=True)
    viewcount = models.IntegerField(null=True, default=0)
    sellcount = models.IntegerField(null=True, default=0)

    def sell_ratio(self):
        if not self.viewcount == 0:
            return round(float(self.sellcount) / float(self.viewcount), 4) * 100
        else:
            return 0
