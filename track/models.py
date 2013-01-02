#coding=utf-8
import ast
from datetime import timedelta

from django.db import models

from project.models import Project, Action
from session.models import Session
from referrer.models import Site, Keyword
from datapanel.utils import parse_url


class Track(models.Model):
    """
    User behavior action track
    ALTER TABLE `datapanel`.`track_track` DROP COLUMN `event` , DROP COLUMN `xpath` , ADD COLUMN `from_track` INT NOT NULL DEFAULT 0  AFTER `url` ;

    update track_trackgroupbyvalue set name = 'referrer_keyword' where name = 'referer_keyword';
    update track_trackgroupbyvalue set name = 'referrer_site' where name = 'referer_site';
    update track_trackgroupbyvalue set name = 'referrer' where name = 'referer';

    ALTER TABLE `track_track`
    ADD COLUMN `project_id` INT(11) NOT NULL AFTER `id`,
    ADD INDEX `track_track_project` (`project_id`);
    """
    project = models.ForeignKey(Project, related_name='track')
    session = models.ForeignKey(Session, related_name='track', verbose_name=u'用户会话')
    action = models.ForeignKey(Action, related_name='track', verbose_name=u'事件')
    url = models.CharField(max_length=255, verbose_name=u'url', default='')
    from_track = models.ForeignKey("Track", null=True)

    # referrer
    referrer_site = models.ForeignKey(Site, related_name='track', null=True)
    referrer_keyword = models.ForeignKey(Keyword, related_name='track', null=True)

    # xpath = models.CharField(max_length=255, verbose_name=u'dom', default='')
    # event = models.CharField(max_length=255, verbose_name=u'event', default='')
    # param = models.TextField(verbose_name=u'参数', default='')
    # mark = models.SmallIntegerField(max_length=2, verbose_name=u'统计参数', null=False, default=0)
    # is_landing = models.SmallIntegerField(max_length=1, verbose_name=u'是否landing', null=False, default=0)
    step = models.IntegerField(max_length=50, null=False, default=0)
    timelength = models.IntegerField(max_length=50, null=False, default=0)
    dateline = models.DateTimeField(auto_now_add=True)

    def set_referrer(self, referrer_string, save=True):
        url = parse_url(referrer_string)

        s = Site.objects.get_or_create(name=url['netloc'])
        self.referrer_site_id = s[0].id

        s = Keyword.objects.get_or_create(name=url['kw'])
        self.referrer_keyword_id = s[0].id

        if save:
            self.save()
        return None

    def set_value(self, name, value, save=True):
        try:
            tvt = TrackValueType.objects.get_or_create(project=self.session.project, name=name)
            tv = TrackValue.objects.get_or_create(track=self, valuetype=tvt[0])
            tv[0].value = value
            if save:
                tv[0].save()
            return tv[0]
        except:
            return None

    def get_value(self, name):
        try:
            tv = TrackValue.objects.get(track=self, valuetype__name=name)
            return tv.value
        except TrackValue.DoesNotExist:
            return ""

    def param_display(self):
        try:
            param = ast.literal_eval(self.param)
            return param
        except:
            return None

    def prev_track(self):
        try:
            return self.session.track.filter(id__lt=self.id).order_by('-id')[0]
        except:
            return None

    def next_track(self):
        try:
            return self.session.track.filter(id__gt=self.id).order_by('id')[0]
        except:
            return None

    def to_tracks(self):
        return self.models.objects.filter(from_track=self)

    def set_from_track(self, referrer_string, save=True):
        probably_from_tracks = self.session.track.filter(id__lt=self.id,
                                                         url=referrer_string)
        if not probably_from_tracks:
            probably_from_tracks = self.session.track.filter(
                id__lt=self.id).order_by('-id')

        if probably_from_tracks:
            self.from_track = probably_from_tracks[0]
        else:
            self.from_track = self

        if save:
            self.save()
        return self.from_track

    def set_timelength(self, save=True):
        next_track = self.next_track()
        # set timelength
        if next_track:
            timelength = next_track.dateline - self.dateline
            self.timelength = timelength.seconds + 1
            if save:
                self.save()
            return self.timelength
        else:
            return 0

    def set_prev_timelength(self, save=True):
        prev_track = self.prev_track()
        # set timelength
        if prev_track:
            timelength = self.dateline - prev_track.dateline
            prev_track.timelength = timelength.seconds + 1
            if save:
                prev_track.save()
            return prev_track.timelength
        else:
            return 0


class TrackValueType(models.Model):
    project = models.ForeignKey(Project, related_name='trackvaluetype')
    name = models.CharField(max_length=20, verbose_name=u'参数', default='')


class TrackValue(models.Model):
    """
    trackvalue from params
    """
    track = models.ForeignKey(Track, related_name='value')
    valuetype = models.ForeignKey(TrackValueType, related_name='value', null=True)
    value = models.TextField(verbose_name=u'值')

    class Meta:
        unique_together = (('track', 'valuetype'), )


class GAction(models.Model):
    """
    Brand new Trackgroup only contained data grouped by action, hour, count
    removed other kinds of data such as: url, average timelength

    ALTER TABLE `datapanel`.`datapanel_trackgroupbyclick` RENAME TO  `datapanel`.`datapanel_trackgroupbycondition` ;
    """
    project = models.ForeignKey(Project, related_name='trackgroupbyaction')
    action = models.ForeignKey(Action, related_name='trackgroupbyaction', verbose_name=u'事件')
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)
    # condition = models.ForeignKey("TrackCondition", related_name='trackgroup', verbose_name=u'满足条件表达式', null=True, blank=True)


class GValue(models.Model):
    """
    TrackGroupbyValue, likes TrackGroupByCondition
    """
    project = models.ForeignKey(Project, related_name='trackgroupbyvalue')
    valuetype = models.ForeignKey(TrackValueType, related_name='gvalue', null=True)
    value = models.CharField(u'参数值', max_length=255, null=False, default='')
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)


class GReferrerSiteAndAction(models.Model):
    '''
    Group by Session ReferrerSite and Time and Action
    '''
    project = models.ForeignKey(Project, related_name='GReferrerSiteAndAction')
    action = models.ForeignKey(Action, related_name='GReferrerSiteAndAction', verbose_name=u'事件')
    referrer_site = models.ForeignKey(Site, related_name='GReferrerSiteAndAction', null=True)
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)


class GReferrerKeywordAndAction(models.Model):
    '''
    Group by Session Referrer Keyword and Time and Action
    '''
    project = models.ForeignKey(Project, related_name='GReferrerKeywordAndAction')
    action = models.ForeignKey(Action, related_name='GReferrerKeywordAndAction', verbose_name=u'事件')
    referrer_keyword = models.ForeignKey(Keyword, related_name='GReferrerKeywordAndAction', null=True)
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)
