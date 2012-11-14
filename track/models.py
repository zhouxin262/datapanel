#coding=utf-8
import ast
from datetime import timedelta

from django.db import models

from project.models import Project, Action
from session.models import Session
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
    session = models.ForeignKey(
        Session, related_name='track', verbose_name=u'用户会话')
    action = models.ForeignKey(
        Action, related_name='track', verbose_name=u'事件')
    url = models.CharField(max_length=255, verbose_name=u'url', default='')
    from_track = models.ForeignKey("Track", null=True)
    # xpath = models.CharField(max_length=255, verbose_name=u'dom', default='')
    # event = models.CharField(max_length=255, verbose_name=u'event', default='')
    # param = models.TextField(verbose_name=u'参数', default='')
    # mark = models.SmallIntegerField(max_length=2, verbose_name=u'统计参数', null=False, default=0)
    # is_landing = models.SmallIntegerField(max_length=1, verbose_name=u'是否landing', null=False, default=0)
    step = models.IntegerField(max_length=50, null=False, default=0)
    timelength = models.IntegerField(max_length=50, null=False, default=0)
    dateline = models.DateTimeField(auto_now_add=True)

    def referrer(self):
        try:
            referrer = self.get_value('referrer')
            referrer_site = self.get_value('referrer_site')
            referrer_keyword = self.get_value('referrer_keyword')

            if not referrer_site and self.from_track:
                referrer = self.from_track.url
                referrer_site = u'站内'
                referrer_keyword = self.from_track.action

            return {'referrer': referrer,
                    'referrer_site': referrer_site,
                    'referrer_keyword': referrer_keyword}
        except IndexError:
            return None

    def set_value(self, name, value, save=True):
        try:
            tv = TrackValue.objects.get_or_create(track=self, name=name)
            tv[0].value = value
            if save:
                tv[0].save()
            return tv[0]
        except:
            return None

    def get_value(self, name):
        try:
            tv = TrackValue.objects.get(track=self, name=name)
            return tv.value
        except TrackValue.DoesNotExist:
            return ""

    # def set_condition_result(self, condition, result):
    #     tcr = TrackConditionResult.objects.get_or_create(track=self, condition=condition)
    #     tcr[0].result = result
    #     tcr[0].save()
    #     return tcr[0]
    #
    # def get_condition_result(self, condition):
    #     try:
    #         tcr = TrackConditionResult.objects.get(track=self, condition=condition)
    #         return tcr.result
    #     except TrackConditionResult.DoesNotExist:
    #         return None
    #
    # def action_display(self):
    #     return smart_decode(slef.action).encode('utf-8')

    def get_time(self, datetype):
        if self.dateline:
            self.hour = self.dateline.replace(
                minute=0, second=0, microsecond=0)
            self.day = self.dateline.replace(
                hour=0, minute=0, second=0, microsecond=0)
            self.week = self.dateline.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
                days=self.dateline.weekday())
            self.month = self.dateline.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0)
            return getattr(self, datetype)
        else:
            return None

    def param_display(self):
        try:
            param = ast.literal_eval(self.param)
            referrer_dict = parse_url(param['referrer'])
            param['referrer_site'] = referrer_dict['netloc']
            param['referrer_keyword'] = referrer_dict['kw']
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

    def set_from_track(self, save=True):
        probably_from_tracks = self.session.track.filter(id__lt=self.id,
                                                         url=self.get_value('referrer')).order_by('id')
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
            # don't care the break
            # if timelength.seconds < 900:
            # 15min no move, definitely away from keyboard!
            #
            self.timelength = timelength.seconds + 1
            if save:
                self.save()

    def set_prev_timelength(self, save=True):
        prev_track = self.prev_track()
        # set timelength
        if prev_track:
            timelength = self.dateline - prev_track.dateline
            # don't care the break
            # if timelength.seconds < 900:
            # 15min no move, definitely away from keyboard!
            #
            prev_track.timelength = timelength.seconds + 1
            if save:
                prev_track.save()


class TrackValue(models.Model):
    """
    update track_trackvalue set name = 'referrer_site' where name = 'referer_site';
    update track_trackvalue set name = 'referer_keyword' where name = 'referer_keyword';
    update track_trackvalue set name = 'referer' where name = 'referer'
    """
    track = models.ForeignKey(Track, related_name='value')
    name = models.CharField(max_length=20, verbose_name=u'参数')
    value = models.TextField(verbose_name=u'值')

    class Meta:
        unique_together = (('track', 'name'), )


class GAction(models.Model):
    """
    Brand new Trackgroup only contained data grouped by action, hour, count
    removed other kinds of data such as: url, average timelength

    ALTER TABLE `datapanel`.`datapanel_trackgroupbyclick` RENAME TO  `datapanel`.`datapanel_trackgroupbycondition` ;
    """
    project = models.ForeignKey(Project, related_name='trackgroupbyaction')
    action = models.ForeignKey(
        Action, related_name='trackgroupbyaction', verbose_name=u'事件')
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
    name = models.CharField(max_length=20, verbose_name=u'参数名', default='')
    value = models.CharField(u'参数值', max_length=255, null=False, default='')
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)


class GReferrerSiteAndAction(models.Model):
    '''
    Group by Session ReferrerSite and Time and Action
    '''
    project = models.ForeignKey(Project, related_name='trackgroupbyReferrerSiteandaction')
    action = models.ForeignKey(
        Action, related_name='sessiongroupbyReferrerSite', verbose_name=u'事件')
    value = models.CharField(max_length=255, verbose_name=u'来源网站', default='')
    datetype = models.CharField(u'统计时间', null=False, max_length=12)
    dateline = models.DateTimeField(verbose_name=u"时间", max_length=13, null=False)
    count = models.IntegerField(u'统计数值', null=False, default=0)
    timelength = models.IntegerField(u'访问时长', null=False, default=0)
