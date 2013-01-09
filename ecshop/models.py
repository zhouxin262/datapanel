#coding=utf8
from django.db import models

from datapanel.models import Timeline
from project.models import Project
from session.models import Session


class OrderManager(models.Manager):
    def process(self, project, session, order_sn, order_amount=0, goods_list={}, *args, **kwargs):
        order = OrderInfo()
        order.project = project
        order.session = session
        order.order_sn = order_sn
        order.order_amount = order_amount
        order.save()

        for goods_id, goods_number in goods_list.items():
            og = OrderGoods()
            og.project = project
            og.session = session
            og.order = order
            og.goods_id = goods_id
            og.goods_number = goods_number
            og.save()


class OrderInfo(models.Model):
    project = models.ForeignKey(Project, related_name='esc_orderinfo')
    session = models.ForeignKey(Session, related_name='esc_orderinfo')
    order_sn = models.CharField(max_length=50, verbose_name=u"订单编号")
    order_amount = models.DecimalField(null=True, max_digits=11, decimal_places=3, default=0)
    dateline = models.DateTimeField(auto_now_add=True, null=True)

    objects = OrderManager()


class OrderGoods(models.Model):
    project = models.ForeignKey(Project, related_name='esc_ordergoods')
    session = models.ForeignKey(Session, related_name='esc_ordergoods')
    order = models.ForeignKey(OrderInfo, related_name='esc_ordergoods')
    goods_id = models.IntegerField(null=True, default=0)
    goods_number = models.IntegerField(null=True, default=0)


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


class Report1(models.Model):
    """ overview """
    project = models.ForeignKey(Project, related_name='esc_report1')
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    timeline = models.ForeignKey(Timeline, null=True)
    userview = models.IntegerField(u'UV', null=True, default=0)
    pageview = models.IntegerField(u'PV', null=True, default=0)
    goodsview = models.IntegerField(u'访问产品的个数', null=True, default=0)
    goodspageview = models.IntegerField(u'产品页访问数', null=True, default=0)
    ordercount = models.IntegerField(u'订单量', null=True, default=0)
    ordergoodscount = models.IntegerField(u'订单商品件数', null=True, default=0)
    orderamount = models.IntegerField(u'订单总额', null=True, default=0)

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


class Report2(models.Model):
    """
    Goods Report
    including goodsview and goods selling data
    """
    project = models.ForeignKey(Project, related_name='esc_report2')
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    timeline = models.ForeignKey(Timeline, null=True)
    goods_id = models.IntegerField(null=True, default=0)
    viewcount = models.IntegerField(null=True, default=0)
    sellcount = models.IntegerField(null=True, default=0)

    def sell_ratio(self):
        if not self.viewcount == 0:
            return round(float(self.sellcount) / float(self.viewcount), 5) * 1000
        else:
            return 0
