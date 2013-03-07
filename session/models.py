# coding=utf-8
from datetime import datetime

from django.db import models
from django.utils.crypto import get_random_string
from django.db.models import Avg, Count
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import Project
from referrer.models import Site, Keyword
from datapanel.models import Timeline
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


class SessionManager(models.Manager):
    def exists(self, session_key):
        return Session.objects.filter(session_key=session_key).exists()

    def _get_new_session_key(self):
        "Returns session key that isn't being used."
        # Todo: move to 0-9a-z charset in 1.5
        hex_chars = '1234567890abcdef'
        # session_key should not be case sensitive because some backends
        # can store it on case insensitive file systems.
        while True:
            session_key = get_random_string(32, hex_chars)
            if not self.exists(session_key):
                break
        return session_key

    def create_new(self, project=None):
        while True:
            obj = Session()
            obj.session_key = self._get_new_session_key()
            if project:
                obj.project = project
            # try:
            obj.save()
            # except:
            #     continue
            return obj


class AbsSession(models.Model):
    """
    Abstract Session Model
    Session, SessionArch
    """
    project = models.ForeignKey(Project, null=True, blank=True, default=None)
    session_key = models.CharField(unique=True, max_length=40, verbose_name=u'用户会话', default='')
    permanent_session_key = models.CharField(max_length=40, verbose_name=u'用户记录', default='')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'会话开始时间')
    end_time = models.DateTimeField(auto_now=True, verbose_name=u'会话结束时间')
    user_language = models.CharField(max_length=255, verbose_name=u'客户端语言', default='')
    user_timezone = models.CharField(max_length=255, verbose_name=u'客户端时区', default='')

    # client
    agent = models.ForeignKey(UserAgent, null=True)
    os = models.ForeignKey(UserOS, null=True)
    device = models.ForeignKey(UserDevice, null=True)

    # referrer
    referrer_site = models.ForeignKey(Site, null=True)
    referrer_keyword = models.ForeignKey(Keyword, null=True)

    track_count = models.IntegerField(verbose_name=u'浏览页面数量', default=0)
    timelength = models.IntegerField(verbose_name=u'访问时长', default=0)
    ipaddress = models.IPAddressField(verbose_name=u'IP地址', null=False, default='0.0.0.0')

    def first_track(self):
        try:
            return self.track_set.filter().order_by('id')[0]
        except IndexError:
            return None

    def last_track(self):
        try:
            return self.track_set.filter().order_by('-id')[0]
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
        for t in self.track_set.filter().order_by('id'):
            if prev_track:
                if (prev_track.timelength == 0 or prev_track.timelength > 300) and (t.dateline - prev_track.dateline).seconds > 300:
                    tracks[-1][1] += u"</li><span class='break'>%d 分钟</span>" % ((t.dateline -
                                                                                 prev_track.dateline).seconds / 60)
                    tracks.append([t.action.name, "<span class='type-name'>%s</span>" % t.action.name])
                else:
                    if t.action == prev_track.action:
                        # tracks[0][1] = "aaaaa"
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
            self.week = self.start_time.replace(
                hour=0, minute=0, second=0, microsecond=0) - timedelta(days=self.start_time.weekday())
            self.month = self.start_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return getattr(self, datetype)
        else:
            return None

    def set_value(self, name, value, save=True):
        try:
            sessionvalueType = SessionValueType.objects.get_or_create(project=self.project, name=name)
            sessionValue = SessionValue.objects.get_or_create(session=self, valuetype=sessionvalueType[0])
            sessionValue[0].value = value
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

    def set_referrer(self, referrer_url, save=True):
        referrer = parse_url(referrer_url)
        s = Site.objects.get_or_create(name=referrer.get('d'))
        self.referrer_site_id = s[0].id
        s = Keyword.objects.get_or_create(name=referrer.get('kw'))
        self.referrer_keyword_id = s[0].id
        if save:
            self.save()
        return None

    class Meta:
        abstract = True


class Session(AbsSession):
    """
    User sessions
    """
    objects = SessionManager()


class SessionArch(AbsSession):
    """
    User sessions archive
    """
    pass


class SessionValueType(models.Model):
    project = models.ForeignKey(Project, related_name='sessionvaluetype')
    name = models.CharField(max_length=20, verbose_name=u'参数', default='')


class AbsSessionValue(models.Model):
    valuetype = models.ForeignKey(SessionValueType, null=True)
    value = models.TextField(verbose_name=u'值', default='')

    class Meta:
        abstract = True
        unique_together = (('session', 'valuetype'), )


class SessionValue(AbsSessionValue):
    session = models.ForeignKey(Session)


class SessionValueArch(AbsSessionValue):
    session = models.ForeignKey(SessionArch)


class GTimeManager(models.Manager):
    def generate(self, project, timeline, save=False):
        try:
            r = GTime.objects.get(project=project, timeline=timeline)
        except GTime.DoesNotExist:
            r = GTime()
            r.project = project
            r.timeline = timeline

        drange = timeline.get_range()

        s = Session.objects.filter(
            project=project, end_time__range=drange).aggregate(Count("id"), Avg('track_count'), Avg('timelength'))
        r.count = s['id__count']
        r.track_count = s['track_count__avg']
        r.timelength = s['timelength__avg']

        if save:
            r.save()
        return r

    def cache(self, project, timeline):
        key = "gtime|p:" + str(project.id) + "|d:" + timeline.datetype
        value = cache.get(key, {"timeline": None, "data": None})
        if value and value['timeline']:
            in_time = value['timeline'].has_time(datetime.now())
            if not in_time:
                value['data'].save()
                value['data'] = None
        if not value['data']:
            value = {'timeline': timeline, 'data': GTime.objects.generate(project, timeline)}
            cache.set(key, value)
        return (key, value)


@receiver(post_save)
def gtime_receiver(sender, instance, created, **kwargs):
    if sender.__name__ in ('Session', 'Track') and created:
        for datetype in ['hour', 'day']:
            s = datetime.now().replace(minute=0, second=0, microsecond=0)
            if datetype == 'day':
                s = s.replace(hour=0)
            timeline = Timeline.objects.get_or_create(datetype=datetype, dateline=s)[0]

            (key, value) = GTime.objects.cache(instance.project, timeline)
            if sender.__name__ == 'Session':
                value.count += 1
            elif sender.__name__ == 'Track':
                value.track_count = float(value.track_count * value.count + 1) / value.count
                try:
                    value.timelength = float(value.timelength * value.count + instance.prev_track().timelength) / value.count
                except:
                    pass
            cache.set(key, value)


class GTime(models.Model):
    '''
    Session Group by Time
    G stands for group by
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbytime')
    timeline = models.ForeignKey(Timeline, null=True)
    count = models.IntegerField(u'统计数值', null=True, default=0)
    track_count = models.IntegerField(u'点击数', null=True, default=0)
    timelength = models.IntegerField(u'访问时长', null=True, default=0)

    objects = GTimeManager()


class GReferrerSite(models.Model):
    '''
    Session Group by ReferrerSite and Time
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbyReferrerSite')
    timeline = models.ForeignKey(Timeline, null=True)
    referrer_site = models.ForeignKey(Site, related_name='GReferrerSite', null=True)
    count = models.IntegerField(u'统计数值', default=0, null=True)
    track_count = models.IntegerField(u'点击数', default=0, null=True)
    timelength = models.IntegerField(u'访问时长', default=0, null=True)


class GReferrerKeyword(models.Model):
    '''
    Session Group by ReferrerSite and Time
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbyReferrerkeyword')
    timeline = models.ForeignKey(Timeline, null=True)
    referrer_keyword = models.ForeignKey(Keyword, related_name='GReferrerKeyword', null=True)
    count = models.IntegerField(u'统计数值', default=0, null=True)
    track_count = models.IntegerField(u'点击数', default=0, null=True)
    timelength = models.IntegerField(u'访问时长', default=0, null=True)
