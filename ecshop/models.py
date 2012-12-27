#coding=utf8
from django.db import models

from project.models import Project
from session.models import Session


class OrderInfo(models.Model):
    project = models.ForeignKey(Project, related_name='esc_orderinfo')
    session = models.ForeignKey(Session, related_name='esc_orderinfo')
    order_sn = models.CharField(max_length=50, verbose_name=u"订单编号")
    order_amount = models.DecimalField(null=True, max_digits=11, decimal_places=3, default=0)


class OrderGoods(models.Model):
    project = models.ForeignKey(Project, related_name='esc_ordergoods')
    session = models.ForeignKey(Session, related_name='esc_ordergoods')
    order = models.ForeignKey(OrderInfo, related_name='esc_ordergoods')
    goods_id = models.IntegerField(null=True, default=0)
    goods_number = models.IntegerField(null=True, default=0)
