#coding=utf-8
import ast, urlparse
from datetime import datetime, timedelta, tzinfo
from django.db import models
from django.contrib.auth.models import User
from datapanel.utils import smart_decode

class Project(models.Model):
    """docstring for Project"""
    name = models.CharField(max_length=20, verbose_name=u'项目名称')
    url = models.CharField(max_length=255, verbose_name=u'项目URL')
    dateline = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    lastview = models.DateTimeField(verbose_name=u'最后访问时间', auto_now=True)
    creator = models.ForeignKey(User, verbose_name=u'创建用户', related_name='create_project')
    participants = models.ManyToManyField(User, verbose_name=u'参与用户', related_name='participate_projects')
    key = models.CharField(max_length=255, verbose_name=u'', default='')
    token = models.CharField(max_length=255, verbose_name=u'', default='')

    class Meta:
        unique_together = (('name', 'creator'),)
        ordering = ['-lastview']

    def __unicode__(self):
        return self.name

class Action(models.Model):
    """
    Websites' managers defined their own actions
    """
    project = models.ForeignKey(Project, related_name='action')
    name = models.CharField(max_length=255, verbose_name=u'行为名称')
    url = models.CharField(max_length=255, verbose_name=u'URL正则', null=True, blank=True)
    xpath = models.CharField(max_length=255, verbose_name=u'控件', null=True,  blank=True)
    event = models.CharField(max_length=255, verbose_name=u'事件', null=True, blank=True)

    def __unicode__(self):
        return self.name

class Session(models.Model):
    """
    User sessions
    ALTER TABLE `datapanel`.`datapanel_session`
    ADD INDEX `datapanel_session_trackcount` (`track_count` ASC) ;

    ALTER TABLE `datapanel`.`datapanel_session` ADD COLUMN `stream_str` TEXT NULL  AFTER `ipaddress` ;
    """
    project = models.ForeignKey(Project, related_name='session')
    sn = models.CharField(unique=True, max_length=40, verbose_name=u'用户会话', default='')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'会话开始时间')
    end_time = models.DateTimeField(auto_now=True, verbose_name=u'会话结束时间')
    user_language = models.CharField(max_length=255, verbose_name=u'客户端语言', default='')
    user_timezone = models.CharField(max_length=255, verbose_name=u'客户端时区', default='')
    user_agent = models.CharField(max_length=255, verbose_name=u'客户端类型', default='')
    user_referer = models.CharField(max_length=255, verbose_name=u'客户端来源', default='')
    track_count = models.IntegerField(verbose_name=u'浏览页面数量', default=0)
    ipaddress = models.IPAddressField(verbose_name=u'IP地址', null=False, default='0.0.0.0')
#    stream_str = models.TextField(verbose_name=u'访问流') # for calculate the convert ratio

    def first_track(self):
        try:
            return self.track.filter().order_by('id')[0]
        except IndexError:
            return None

    def last_track(self):
        try:
            return self.track.filter().order_by('-id')[0]
        except IndexError:
            return None

    def first_referer(self):
        try:
            return TrackValue.objects.filter(name='referer_site', track__session = self).order_by('track__id')[0].track.param_display()
        except IndexError:
            return None

    def last_referer(self):
        try:
            return TrackValue.objects.filter(name='referer_site', track__session = self).order_by('-track__id')[0].track.param_display()
        except IndexError:
            return None

    def get_stream_display(self):
        actions = [action.name for action in Action.objects.filter(project=self.project)]
        tracks = []
        prev_track = None
        for t in self.track.all().order_by('id'):
            if prev_track:
                if (prev_track.timelength == 0 or prev_track.timelength > 300) and (t.dateline - prev_track.dateline).seconds > 300:
                    tracks[-1][1] += u"</li><span class='break'>%d 分钟</span>" % ((t.dateline - prev_track.dateline).seconds / 60 )
                    tracks.append([t.action, "<span class='type-name'>%s</span>" % t.action])
                else:
                    if t.action == prev_track.action:
                        #tracks[0][1] = "aaaaa"
                        tracks[-1][1] += "<span class='repeat'>*</span>"
                    else:
                        tracks.append([t.action, "<span class='type-name'>%s</span>" % t.action])
            else:
                tracks.append([t.action, "<span class='type-name'>%s</span>" % t.action])
            prev_track = t
        return "".join(["<li class='stream-block background-%02d'>%s</li>" % ((actions.index(t[0]) + 1) * 7 % 30, t[1]) for t in tracks])

class Track(models.Model):
    """
    User behavior action track
    """
    session = models.ForeignKey(Session, related_name='track', verbose_name=u'用户会话')
    action = models.CharField(max_length=255, verbose_name=u'事件', default='')
    url = models.CharField(max_length=255, verbose_name=u'url', default='')
    xpath = models.CharField(max_length=255, verbose_name=u'dom', default='')
    event = models.CharField(max_length=255, verbose_name=u'event', default='')
    param = models.CharField(max_length=255, verbose_name=u'参数', default='')
    # mark = models.SmallIntegerField(max_length=2, verbose_name=u'统计参数', null=False, default=0)
    # is_landing = models.SmallIntegerField(max_length=1, verbose_name=u'是否landing', null=False, default=0)
    step = models.IntegerField(max_length=50,null=False,default=0)
    timelength = models.IntegerField(max_length=50, null=False, default=0)
    dateline = models.DateTimeField(auto_now_add=True)
    hourline = models.DateTimeField(auto_now_add=False, verbose_name=u"小时")
    dayline = models.DateTimeField(auto_now_add=False, verbose_name=u"天")
    weekline = models.DateTimeField(auto_now_add=False, verbose_name=u"周")
    monthline = models.DateTimeField(auto_now_add=False, verbose_name=u"月")

    def set_value(self, name, value):
        try:
            tv = TrackValue.objects.get_or_create(track=self, name=name)
            tv[0].value = value
            tv[0].save()
            return tv[0]
        except:
            return None

    def get_value(self, name):
        try:
            tv = TrackValue.objects.get(track=self, name=name)
            return tv.value
        except TrackValue.DoesNotExist:
            return None

    def set_condition_result(self, condition, result):
        tcr = TrackConditionResult.objects.get_or_create(track = self, condition=condition)
        tcr[0].result = result
        tcr[0].save()
        return tcr[0]

    def get_condition_result(self, condition):
        try:
            tcr = TrackConditionResult.objects.get(track = self, condition=condition)
            return tcr.result
        except TrackConditionResult.DoesNotExist:
            return None


    def action_display(self):
        return smart_decode(slef.action).encode('utf-8')

    def set_times(self, save=False):
        if self.dateline:
            self.hourline = self.dateline.replace(minute=0, second=0, microsecond=0)
            self.dayline = self.dateline.replace(hour=0, minute=0, second=0, microsecond=0)
            self.weekline = self.dateline.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
                days=self.dateline.weekday())
            self.monthline = self.dateline.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if save:
                self.save()
            else:
                return True
        else:
            return False

    def param_display(self):
        try:
            param = ast.literal_eval(self.param)
            parsed_url = urlparse.urlparse(param['referer'])
            if parsed_url.netloc and parsed_url.netloc != 'www.xmeise.com':
                param['referer_site'] = parsed_url.netloc
                querystring = urlparse.parse_qs(parsed_url.query, True)
                if parsed_url.netloc.find('baidu') != -1:
                    #baidu
                    if querystring.has_key('wd'):
                        param['referer_keyword'] = smart_decode(querystring['wd'][0])
                    elif querystring.has_key('word'):
                        param['referer_keyword'] = smart_decode(querystring['word'][0])
                if parsed_url.netloc.find('sogou') != -1:
                    #sogou
                    if querystring.has_key('query'):
                        param['referer_keyword'] = smart_decode(querystring['query'][0])
            return param
        except:
            return None

    def prev_track(self):
        try:
            return self.session.track.filter(id__lt=self.id)[0]
        except:
            return None

    def next_track(self):
        try:
            return self.session.track.filter(id__gt=self.id).order_by('id')[0]
        except:
            return None

class TrackCondition(models.Model):
    """
    TrackCondition
    only support 'equal' condition for now
    """
    project = models.ForeignKey(Project, related_name='trackcondition')
    name = models.CharField(max_length=20, verbose_name=u'条件命名')

    def run_test(self, track):
        test_result = False
        for i, tester in enumerate(self.tracktester.all()):
            result = False
            if tester.test_operator == 'gt':
                result = getattr(track, tester.col_name) > int(tester.test_value)
            elif tester.test_operator == 'eq':
                result = getattr(track, tester.col_name) == int(tester.test_value)
            elif tester.test_operator == 'lt':
                result = getattr(track, tester.col_name) < int(tester.test_value)

            if i == 0:
                test_result = result

            if tester.operator == "AND":
                test_result = test_result and result
            else:
                test_result = test_result or result

        return test_result


class TrackConditionTester(models.Model):
    """
    TrackConditionTester
    should be regex tester.
    """
    OPERATOR_CHOICES = (('OR', 'OR'), ('AND', 'AND'))
    TESTEROPERATOR_CHOICES = (('gt', '大于'), ('eq', '等于'), ('lt', '小于'))
    COLNAME_CHOICES = (('action', '动作名称'), ('step', '操作步骤'), ('mark', '标志'))
    condition = models.ForeignKey(TrackCondition, related_name='tracktester')
    operator = models.CharField(max_length=20, verbose_name="与或关系", choices=OPERATOR_CHOICES)
    col_name = models.CharField(max_length=20, verbose_name=u'Track列名', choices=COLNAME_CHOICES)
    test_operator = models.CharField(max_length=255, verbose_name=u'运算符', choices=TESTEROPERATOR_CHOICES)
    test_value = models.CharField(max_length=255, verbose_name=u'值') # 以后考虑改成正则表达式

class TrackGroupByCondition(models.Model):
    """
    Brand new Trackgroup only contained data grouped by action, hour, count
    removed other kinds of data such as: url, average timelength

    ALTER TABLE `datapanel`.`datapanel_trackgroupbyclick` RENAME TO  `datapanel`.`datapanel_trackgroupbycondition` ;
    """
    project = models.ForeignKey(Project, related_name='trackgroupbycondition')
    action = models.CharField(max_length=255, verbose_name=u'事件', default='')
    datetype = models.CharField(u'统计时间', null=True, max_length=12)
    value = models.IntegerField(u'统计数值', null=True)
    dateline = models.IntegerField(verbose_name=u"时间")
    condition = models.ForeignKey("TrackCondition", related_name='trackgroup', verbose_name=u'满足条件表达式', null=True, blank=True)

    def increase_value(self, save=True):
        if self.value:
            self.value = self.value+1
        else:
            self.value = 1

        if save:
            self.save()
        return self.value

class TrackValue(models.Model):
    track = models.ForeignKey(Track, related_name='value')
    name = models.CharField(max_length=20, verbose_name=u'参数')
    value = models.CharField(max_length=255, verbose_name=u'值')

    class Meta:
        unique_together = (('track', 'name'), )

class TrackGroupByValue(models.Model):
    """
    TrackGroupbyValue, likes TrackGroupByCondition
    """
    project = models.ForeignKey(Project, related_name='trackgroupbyvalue')
    name = models.CharField(max_length=255, verbose_name=u'参数名', default='')
    value = models.CharField(u'参数值', max_length=255, null=True)
    datetype = models.CharField(u'统计时间', null=True, max_length=12)
    count = models.IntegerField(u'统计数值', null=True)
    dateline = models.IntegerField(verbose_name=u"时间")

    def increase_value(self, save=True):
        if self.count:
            self.count = self.count+1
        else:
            self.count = 1

        if save:
            self.save()
        return self.count


class TrackConditionResult(models.Model):
    track = models.ForeignKey(Track, related_name='trackconditionresult')
    condition = models.ForeignKey(TrackCondition, related_name='trackconditionresult', verbose_name=u'满足条件表达式')
    result = models.BooleanField(verbose_name=u'条件比对结果', default=False)

class SessionCondition(models.Model):
    """
    SessionCondition
    """
    project = models.ForeignKey(Project, related_name='sessioncondition')
    name = models.CharField(max_length=20,verbose_name=u'条件命名')

class SessionConditionTester(models.Model):
    """
    TrackConditionTester
    should be regex tester.
    """
    OPERATOR_CHOICES = (('OR', 'OR'), ('AND', 'AND'))
    TESTEROPERATOR_CHOICES = (('gt', '大于'), ('eq', '等于'), ('lt', '小于'))
    COLNAME_CHOICES = (('action', '动作名称'), ('param_payway', '操作步骤'), ('mark', '标志'))
    condition = models.ForeignKey(SessionCondition, related_name='sessiontester')
    operator = models.CharField(max_length=20, verbose_name="与或关系", choices=OPERATOR_CHOICES)
    col_name = models.CharField(max_length=20, verbose_name=u'Track列名', choices=COLNAME_CHOICES)
    test_operator = models.CharField(max_length=255, verbose_name=u'运算符', choices=TESTEROPERATOR_CHOICES)
    test_value = models.CharField(max_length=255, verbose_name=u'值') # 以后考虑改成正则表达式

class Funnel(models.Model):
    project = models.ForeignKey(Project, related_name='funnel')
    name = models.CharField(u'命名', max_length=20)

class FunnelAction(models.Model):
    funnel = models.ForeignKey(Funnel, related_name='action')
    order = models.IntegerField()
    action = models.ForeignKey(Action, related_name='funnelaction')

class SessionGroupByTime(models.Model):
    project = models.ForeignKey(Project, related_name='sessiongroupbytime')
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    value = models.IntegerField(u'统计数值', null=True)
    dateline = models.DateTimeField(auto_now_add=False, verbose_name=u"月")
