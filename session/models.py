#coding=utf-8
from django.db import models

from project.models import Project
from referrer.models import Site, Keyword
from datapanel.ua_parser import user_agent_parser
from datetime import timedelta
from datapanel.utils import parse_url


class UserAgent(models.Model):
    family = models.CharField(max_length=50, verbose_name=u'浏览器', default='')
    major = models.CharField(max_length=4, default='')
    minor = models.CharField(max_length=4, default='')
    patch = models.CharField(max_length=10, default='')

    class Meta:
        unique_together = (('family', 'major', 'minor', 'patch'))


class UserOS(models.Model):
    family = models.CharField(max_length=50, verbose_name=u'操作系统', default='')
    major = models.CharField(max_length=4, default='')
    minor = models.CharField(max_length=4, default='')
    patch = models.CharField(max_length=10, default='')
    patch_minor = models.CharField(max_length=10, default='')

    class Meta:
        unique_together = (('family', 'major', 'minor', 'patch', 'patch_minor'))


class UserDevice(models.Model):
    family = models.CharField(max_length=50, verbose_name=u'设备', default='')
    is_mobile = models.BooleanField(default=False)
    is_spider = models.BooleanField(default=False)

    class Meta:
        unique_together = (('family', 'is_mobile', 'is_spider'))


class Session(models.Model):
    """
    User sessions
    """
    project = models.ForeignKey(Project, related_name='session')
    sn = models.CharField(unique=True, max_length=40, verbose_name=u'用户会话', default='')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'会话开始时间')
    end_time = models.DateTimeField(auto_now=True, verbose_name=u'会话结束时间')
    user_language = models.CharField(max_length=255, verbose_name=u'客户端语言', default='')
    user_timezone = models.CharField(max_length=255, verbose_name=u'客户端时区', default='')

    # todo remove this
    user_referrer = models.TextField(verbose_name=u'客户端来源', default='')
    user_agent = models.CharField(max_length=255, verbose_name=u'客户端类型', default='')

    # client
    agent = models.ForeignKey(UserAgent, related_name='session', null=True)
    os = models.ForeignKey(UserOS, related_name='session', null=True)
    device = models.ForeignKey(UserDevice, related_name='session', null=True)

    # referrer
    referrer_site = models.ForeignKey(Site, related_name='session', null=True)
    referrer_keyword = models.ForeignKey(Keyword, related_name='session', null=True)

    track_count = models.IntegerField(verbose_name=u'浏览页面数量', default=0)
    timelength = models.IntegerField(verbose_name=u'访问时长', default=0)
    ipaddress = models.IPAddressField(verbose_name=u'IP地址', null=False, default='0.0.0.0')

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

    def first_referrer(self):
        try:
            track = self.first_track()
            return {'referrer': track.get_value('referrer'),
                    'referrer_site': track.get_value('referrer_site'),
                    'referrer_keyword': track.get_value('referrer_keyword')}
        except IndexError:
            return None

    def get_stream_display(self):
        actions = [action.name for action in self.project.action.filter().order_by('id')]
        tracks = []
        prev_track = None
        for t in self.track.all().order_by('id'):
            if prev_track:
                if (prev_track.timelength == 0 or prev_track.timelength > 300) and (t.dateline - prev_track.dateline).seconds > 300:
                    tracks[-1][1] += u"</li><span class='break'>%d 分钟</span>" % ((t.dateline - prev_track.dateline).seconds / 60)
                    tracks.append([t.action.name, "<span class='type-name'>%s</span>" % t.action.name])
                else:
                    if t.action == prev_track.action:
                        #tracks[0][1] = "aaaaa"
                        tracks[-1][1] += "<span class='repeat'>*</span>"
                    else:
                        tracks.append([t.action.name, "<span class='type-name'>%s</span>" % t.action.name])
            else:
                tracks.append([t.action.name, "<span class='type-name'>%s</span>" % t.action.name])
            prev_track = t
        return "".join(["<li class='stream-block background-%02d'>%s</li>" % ((actions.index(t[0]) + 1) * 7 % 30, t[1]) for t in tracks])

    def get_time(self, datetype):
        if self.start_time:
            self.hour = self.start_time.replace(minute=0, second=0, microsecond=0)
            self.day = self.start_time.replace(hour=0, minute=0, second=0, microsecond=0)
            self.week = self.start_time.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=self.start_time.weekday())
            self.month = self.start_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return getattr(self, datetype)
        else:
            return None

    def set_value(self, name, value, save=True):
        try:
            sessionValue = SessionValue.objects.get_or_create(session=self, name=name, value=value)
            if save:
                sessionValue[0].save()
            return sessionValue[0]
        except SessionValue.DoesNotExist:
            return None

    def get_value(self, name):
        try:
            sessionValues = SessionValue.objects.filter(session=self, name=name)
            return sessionValues
        except SessionValue.DoesNotExist:
            return None

    def set_user_agent(self, user_agent_string, save=True):
        self.user_agent = user_agent_string
        parsed = user_agent_parser.Parse(user_agent_string)
        for name, obj in parsed.items():
            T = None
            if name == 'user_agent':
                T = UserAgent
                f = 'agent'
            elif name == 'os':
                T = UserOS
                f = 'os'
            elif name == 'device':
                T = UserDevice
                f = 'device'
            else:
                continue

            args = {}
            for k, v in obj.items():
                if v is None:
                    v = ''
                args[k] = v

            t = T.objects.get_or_create(**args)
            setattr(self, f + '_id', t[0].id)
        if save:
            self.save()
        return None

    def set_referrer(self, referrer_string, save=True):
        url = parse_url(referrer_string)
        self.user_referrer = url['url']

        s = Site.objects.get_or_create(name=url['netloc'])
        self.referrer_site_id = s[0].id

        s = Keyword.objects.get_or_create(name=url['kw'])
        self.referrer_keyword_id = s[0].id

        if save:
            self.save()
        return None


class SessionValue(models.Model):
    session = models.ForeignKey(Session, related_name='value')
    name = models.CharField(max_length=20, verbose_name=u'参数')
    value = models.TextField(verbose_name=u'值')


class GTime(models.Model):
    '''
    Session Group by Time
    G stands for group by
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbytime')
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    count = models.IntegerField(u'统计数值', null=True, default=0)
    track_count = models.IntegerField(u'点击数', null=True, default=0)
    timelength = models.IntegerField(u'访问时长', null=True, default=0)

    class Meta:
        unique_together = (('datetype', 'dateline'),)


class GReferrerSite(models.Model):
    '''
    Session Group by ReferrerSite and Time
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbyReferrerSite')
    referrer_site = models.ForeignKey(Site, related_name='GReferrerSite', null=True)
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    count = models.IntegerField(u'统计数值', default=0, null=True)
    track_count = models.IntegerField(u'点击数', default=0, null=True)
    timelength = models.IntegerField(u'访问时长', default=0, null=True)


class GReferrerKeyword(models.Model):
    '''
    Session Group by ReferrerSite and Time
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbyReferrerkeyword')
    referrer_keyword = models.ForeignKey(Keyword, related_name='GReferrerKeyword', null=True)
    datetype = models.CharField(u'统计时间', max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    count = models.IntegerField(u'统计数值', default=0, null=True)
    track_count = models.IntegerField(u'点击数', default=0, null=True)
    timelength = models.IntegerField(u'访问时长', default=0, null=True)
