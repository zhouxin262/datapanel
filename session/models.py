#coding=utf-8
from django.db import models

from project.models import Project


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
            track = self.first_track()
            return {'referer': track.get_value('referer'),
            'referer_site': track.get_value('referer_site'),
            'referer_keyword': track.get_value('referer_keyword')}
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


class SessionGroupByTime(models.Model):
    project = models.ForeignKey(Project, related_name='sessiongroupbytime')
    datetype = models.CharField(u'统计类型', null=True, max_length=12)
    value = models.IntegerField(u'统计数值', null=True)
    dateline = models.DateTimeField(auto_now_add=False, verbose_name=u"月")