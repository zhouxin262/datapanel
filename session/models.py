#coding=utf-8
from django.db import models

from project.models import Project
from datetime import timedelta

class Session(models.Model):
    """
    User sessions
    ALTER TABLE `datapanel`.`datapanel_session`
    ADD INDEX `datapanel_session_trackcount` (`track_count` ASC) ;

    ALTER TABLE `datapanel`.`datapanel_session` ADD COLUMN `stream_str` TEXT NULL  AFTER `ipaddress` ;
    ALTER TABLE `datapanel`.`session_session` ADD COLUMN `user_referrer_site` VARCHAR(255) NOT NULL  AFTER `user_referrer` , ADD COLUMN `user_referrer_keyword` VARCHAR(45) NOT NULL  AFTER `user_referrer_site` ;
    ALTER TABLE `session_session`
        ALTER `user_referrer` DROP DEFAULT;
    ALTER TABLE `session_session`
        CHANGE COLUMN `user_referrer` `user_referrer` TEXT NOT NULL AFTER `user_agent`;

    ALTER TABLE `session_session`
        ALTER `user_referer_site` DROP DEFAULT,
        ALTER `user_referer_keyword` DROP DEFAULT;
    ALTER TABLE `session_session`
        CHANGE COLUMN `user_referer` `user_referrer` TEXT NOT NULL AFTER `user_agent`,
        CHANGE COLUMN `user_referer_site` `user_referrer_site` VARCHAR(255) NOT NULL AFTER `user_referrer`,
        CHANGE COLUMN `user_referer_keyword` `user_referrer_keyword` VARCHAR(45) NOT NULL AFTER `user_referrer_site`;

    """
    project = models.ForeignKey(Project, related_name='session')
    sn = models.CharField(unique=True, max_length=40, verbose_name=u'用户会话', default='')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=u'会话开始时间')
    end_time = models.DateTimeField(auto_now=True, verbose_name=u'会话结束时间')
    user_language = models.CharField(max_length=255, verbose_name=u'客户端语言', default='')
    user_timezone = models.CharField(max_length=255, verbose_name=u'客户端时区', default='')
    user_agent = models.CharField(max_length=255, verbose_name=u'客户端类型', default='')
    user_referrer = models.CharField(max_length=255, verbose_name=u'客户端来源', default='')
    user_referrer_site = models.CharField(max_length=255, verbose_name=u'来源网站', default='')
    user_referrer_keyword = models.CharField(max_length=255, verbose_name=u'来源关键词', default='')
    track_count = models.IntegerField(verbose_name=u'浏览页面数量', default=0)
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
    dateline = models.IntegerField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    track_count = models.IntegerField(u'点击数', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)
    class Meta:
        unique_together = (('datetype', 'dateline'),)


class GReferrerSite(models.Model):
    '''
    Session Group by ReferrerSite and Time
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbyReferrerSite')
    value = models.CharField(max_length=255, verbose_name=u'来源网站', default='')
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.IntegerField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    track_count = models.IntegerField(u'点击数', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)


class GReferrerKeyword(models.Model):
    '''
    Session Group by ReferrerSite and Time
    '''
    project = models.ForeignKey(Project, related_name='sessiongroupbyReferrerkeyword')
    value = models.CharField(max_length=255, verbose_name=u'来源关键词', default='')
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.IntegerField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    track_count = models.IntegerField(u'点击数', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)

