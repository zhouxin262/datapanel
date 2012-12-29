#coding=utf8
from django.db import models

from project.models import Project
from session.models import Session


class OrderManager(models.Manager):
    def process(self, project, session, order_sn, order_amount=0, goods_list={}, *args, **kwargs):
        print order_sn
        order = OrderInfo()
        order.project = Project.objects.get(id=session.project.id)
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


class Report1(models.Model):
    """ overview """
    project = models.ForeignKey(Project, related_name='esc_report1')
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    name = models.CharField(max_length=50, verbose_name=u"统计内容", null=False, default="")
    count = models.IntegerField(u'统计数值', null=True, default=0)
