#coding=utf-8
import ast
import urlparse
from datetime import datetime, timedelta, tzinfo
from django.db import models
from django.contrib.auth.models import User



# class TrackCondition(models.Model):
#     """
#     TrackCondition
#     only support 'equal' condition for now
#     """
#     project = models.ForeignKey(Project, related_name='trackcondition')
#     name = models.CharField(max_length=20, verbose_name=u'条件命名')

#     def run_test(self, track):
#         test_result = False
#         for i, tester in enumerate(self.tracktester.all()):
#             result = False
#             if tester.test_operator == 'gt':
#                 result = getattr(track, tester.col_name) > int(tester.test_value)
#             elif tester.test_operator == 'eq':
#                 result = getattr(track, tester.col_name) == int(tester.test_value)
#             elif tester.test_operator == 'lt':
#                 result = getattr(track, tester.col_name) < int(tester.test_value)

#             if i == 0:
#                 test_result = result

#             if tester.operator == "AND":
#                 test_result = test_result and result
#             else:
#                 test_result = test_result or result

#         return test_result


# class TrackConditionTester(models.Model):
#     """
#     TrackConditionTester
#     should be regex tester.
#     """
#     OPERATOR_CHOICES = (('OR', 'OR'), ('AND', 'AND'))
#     TESTEROPERATOR_CHOICES = (('gt', '大于'), ('eq', '等于'), ('lt', '小于'))
#     COLNAME_CHOICES = (('action', '动作名称'), ('step', '操作步骤'), ('mark', '标志'))
#     condition = models.ForeignKey(TrackCondition, related_name='tracktester')
#     operator = models.CharField(max_length=20, verbose_name="与或关系", choices=OPERATOR_CHOICES)
#     col_name = models.CharField(max_length=20, verbose_name=u'Track列名', choices=COLNAME_CHOICES)
#     test_operator = models.CharField(max_length=255, verbose_name=u'运算符', choices=TESTEROPERATOR_CHOICES)
#     test_value = models.CharField(max_length=255, verbose_name=u'值')  # 以后考虑改成正则表达式


# class TrackGroupByCondition(models.Model):
#     """
#     Brand new Trackgroup only contained data grouped by action, hour, count
#     removed other kinds of data such as: url, average timelength

#     ALTER TABLE `datapanel`.`datapanel_trackgroupbyclick` RENAME TO  `datapanel`.`datapanel_trackgroupbycondition` ;
#     """
#     project = models.ForeignKey(Project, related_name='trackgroupbycondition')
#     action = models.CharField(max_length=255, verbose_name=u'事件', default='')
#     datetype = models.CharField(u'统计时间', null=True, max_length=12)
#     value = models.IntegerField(u'统计数值', null=True)
#     dateline = models.IntegerField(verbose_name=u"时间")
#     condition = models.ForeignKey("TrackCondition", related_name='trackgroup', verbose_name=u'满足条件表达式', null=True, blank=True)

#     def increase_value(self, save=True):
#         if self.value:
#             self.value = self.value + 1
#         else:
#             self.value = 1

#         if save:
#             self.save()
#         return self.value




# class TrackGroupByValue(models.Model):
#     """
#     TrackGroupbyValue, likes TrackGroupByCondition
#     """
#     project = models.ForeignKey(Project, related_name='trackgroupbyvalue')
#     name = models.CharField(max_length=255, verbose_name=u'参数名', default='')
#     value = models.CharField(u'参数值', max_length=255, null=True)
#     datetype = models.CharField(u'统计时间', null=True, max_length=12)
#     count = models.IntegerField(u'统计数值', null=True)
#     dateline = models.IntegerField(verbose_name=u"时间")

#     def increase_value(self, save=True):
#         if self.count:
#             self.count = self.count + 1
#         else:
#             self.count = 1

#         if save:
#             self.save()
#         return self.count


# class TrackConditionResult(models.Model):
#     track = models.ForeignKey(Track, related_name='trackconditionresult')
#     condition = models.ForeignKey(TrackCondition, related_name='trackconditionresult', verbose_name=u'满足条件表达式')
#     result = models.BooleanField(verbose_name=u'条件比对结果', default=False)


# class SessionCondition(models.Model):
#     """
#     SessionCondition
#     """
#     project = models.ForeignKey(Project, related_name='sessioncondition')
#     name = models.CharField(max_length=20, verbose_name=u'条件命名')


# class SessionConditionTester(models.Model):
#     """
#     TrackConditionTester
#     should be regex tester.
#     """
#     OPERATOR_CHOICES = (('OR', 'OR'), ('AND', 'AND'))
#     TESTEROPERATOR_CHOICES = (('gt', '大于'), ('eq', '等于'), ('lt', '小于'))
#     COLNAME_CHOICES = (('action', '动作名称'), ('param_payway', '操作步骤'), ('mark', '标志'))
#     condition = models.ForeignKey(SessionCondition, related_name='sessiontester')
#     operator = models.CharField(max_length=20, verbose_name="与或关系", choices=OPERATOR_CHOICES)
#     col_name = models.CharField(max_length=20, verbose_name=u'Track列名', choices=COLNAME_CHOICES)
#     test_operator = models.CharField(max_length=255, verbose_name=u'运算符', choices=TESTEROPERATOR_CHOICES)
#     test_value = models.CharField(max_length=255, verbose_name=u'值')  # 以后考虑改成正则表达式


# class SessionGroupByTime(models.Model):
#     project = models.ForeignKey(Project, related_name='sessiongroupbytime')
#     datetype = models.CharField(u'统计类型', null=True, max_length=12)
#     value = models.IntegerField(u'统计数值', null=True)
#     dateline = models.DateTimeField(auto_now_add=False, verbose_name=u"月")
