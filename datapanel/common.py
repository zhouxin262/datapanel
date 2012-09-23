#coding=utf-8
import datetime

from django.db.models import Count,Avg
from datapanel.models import Track, TrackGroup,Session, Project, Referer

def clean_track():
    ts = Track.objects.filter()
    for i, t in enumerate(ts):
        if i % 1000 == 0:
            print i

        try:
            # 清理无效tracks
            t.action = t.action.decode('gbk').encode('gbk')
        except UnicodeEncodeError:
            t.delete()
            continue

    tgs = TrackGroup.objects.filter()
    for i, t in enumerate(tgs):
        if i % 1000 == 0:
            print i

        try:
            # 清理无效tracks
            t.name = t.name.decode('gbk').encode('gbk')
        except UnicodeEncodeError:
            t.delete()
            continue

def session_referer(starttime):
    # 清理无效session
    ss = Session.objects.filter(track__isnull = True).delete()

    ss = Session.objects.filter(start_time__gte = starttime)
    for s in ss:
        t = s.first_track()
        if t and t.param_display():
            p = t.param_display()
            if p and p.has_key('referer_parsed'):
                if not s.referer.all():
                    try:
                        r = Referer()
                        r.session = s
                        r.site = p['referer_site']
                        if p.has_key('referer_keyword'):
                            r.keyword = p['referer_keyword']
                        else:
                            r.keyword = ''
                        r.url = p['referer']
                        r.save()
                    except:
                        print r.keyword

def dealdata():
    # 清理无效session
    ss = Session.objects.filter(track__isnull = True).delete()

    s_list = []
    tn = Track.objects.filter(step = 0)

    for i, t in enumerate(tn):
        try:
            # 清理无效tracks
            t.action = t.action.decode('gbk').encode('gbk')
        except UnicodeEncodeError:
            t.delete()
            continue

        if i % 1000 == 0:
            print (i * 100) / tn.count(), '%'
        t.step = Track.objects.filter(session = t.session, pk__lt = t.pk).count() + 1
        t.save()

    print 'Preprocess with tracks, finished.'

def tongji(starttime='', endtime='', grouptype ='A', datatype = 'C', groupcate = 'A', groupdate='H', save = True):
    # TYPE_CHOICES = (('U', u'url'), ('A', u'action',))
    # DATA_CHOICES = (('C', u'页面点击数'), ('D', u'页面停留时间',))
    # CATE_CHOICES = (('A', u'所有页面'), ('L', u'着陆页',), ('F', u'第一次点击',), ('J', u'跳出页',))
    # DATE_CHOICES = (('H', u'小时'), ('D', u'天',), ('W', u'周 ',), ('M', u'月',), ('Y', u'年',))
    for p in Project.objects.filter():
        args = {}

        if starttime:
            args['dateline__gte'] = starttime
        if endtime:
            args['dateline__lte'] = endtime

        if groupcate == 'L':
            args['mark__in'] = [1,10]
        elif groupcate == 'F':
            args['mark__in'] = [2,20]
        elif groupcate == 'J':
            args['mark__in'] = [10,20,30,40,50,60,70,80,0]
        else:
            pass

        if grouptype == 'A':
            alias = 'action'
        elif grouptype == 'U':
            alias = 'url'
        else:
            alias = 'action'

        for name in Track.objects.filter().values(alias).distinct():
            args[alias + '__exact'] = name[alias]

            if datatype == 'C':
                c = Track.objects.filter(**args).count()
            elif datatype == 'D':
                c = Track.objects.filter(**args).aggregate(Avg('timelength'))['timelength__avg']
            else:
                c = Track.objects.filter(**args).count()

            if save:
                tg = TrackGroup()
                tg.project = p
                tg.grouptype = grouptype
                tg.groupcate = groupcate
                tg.groupdate = groupdate
                tg.datatype = datatype
                tg.name = name[alias]
                if not c:
                    c = 0
                tg.count = int(c)
                tg.dateline = endtime
                tg.save()
                print starttime, endtime, grouptype, datatype, groupcate, groupdate
        return c