#coding=utf8
from django.db import models

from project.models import Project
from session.models import Session


class OrderManager(models.Manager):
    def process(self, project, session, order_sn, order_amount=0, goods_list={}, *args, **kwargs):
        o = OrderInfo()
        o.project = project
        o.session = session
        o.order_sn = order_sn
        o.order_amount = order_amount
        o.save()

        for goods_id, goods_number in goods_list.items():
            og = OrderGoods()
            og.project = project
            og.session = session
            og.order = o
            og.goods_id = goods_id
            og.goods_number = goods_number
            og.save()


class OrderInfo(models.Model):
    project = models.ForeignKey(Project, related_name='esc_orderinfo')
    session = models.ForeignKey(Session, related_name='esc_orderinfo')
    order_sn = models.CharField(max_length=50, verbose_name=u"订单编号")
    order_amount = models.DecimalField(null=True, max_digits=11, decimal_places=3, default=0)
    dateline = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()


class OrderGoods(models.Model):
    project = models.ForeignKey(Project, related_name='esc_ordergoods')
    session = models.ForeignKey(Session, related_name='esc_ordergoods')
    order = models.ForeignKey(OrderInfo, related_name='esc_ordergoods')
    goods_id = models.IntegerField(null=True, default=0)
    goods_number = models.IntegerField(null=True, default=0)
