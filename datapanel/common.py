#coding=utf-8
import datetime

from django.db.models import Count,Avg

from datapanel.models import Track, TrackGroup,Session

def dealtrack(s):
    ts = Track.objects.filter(session = s).order_by('dateline')
    c = ts.count()
    for i in range(0,c):
        tt = ts[i]
        tt.step = i+1
        if (i+1) == c:
            tt.timelength = 0
            if c == 1:
                tt.mark = 10
            elif c == 2:
                tt.mark = 20
            elif tt.action == u'总确认':
                tt.mark = 30
            elif ts[i-1].mark in [31,41,51,61,71]:
                tt.mark = ts[i-1].mark -1 +10
            else:
                tt.mark = 0

        else:
            tl = (ts[i+1].dateline - tt.dateline).seconds
            if tl ==0:
                tt.timelength = 1
            else:
                tt.timelength = tl
            if i == 0:
                tt.mark = 1
            elif i == 1:
                tt.mark = 2
            elif tt.action == u'总确认':
                tt.mark = 31
            elif ts[i-1].mark in [31,41,51,61]:
                tt.mark = ts[i-1].mark +10
            else:
                tt.mark = 3

        tt.save()
    s.save()

def dealdata():
    list = []
    tn = Track.objects.filter(step__isnull = True)
    for t in tn:
        if t.session.id not in list:
            list.append(t.session.id)
    for l in list:
        ss = Session.objects.get(id = l)
        dealtrack(ss)
    print 'Preprocess with tracks, finished.'

def tongji(starttime='', endtime='', grouptype ='A', datatype = 'C', groupcate = 'A', groupdate='H', save = True):
    # TYPE_CHOICES = (('U', u'url'), ('A', u'action',))
    # DATA_CHOICES = (('C', u'页面点击数'), ('D', u'页面停留时间',))
    # CATE_CHOICES = (('A', u'所有页面'), ('L', u'着陆页',), ('F', u'第一次点击',), ('J', u'跳出页',))
    # DATE_CHOICES = (('H', u'小时'), ('D', u'天',), ('W', u'周 ',), ('M', u'月',), ('Y', u'年',))
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

    if datatype == 'C':
        c = Track.objects.filter(**args).values(alias).annotate(val = Count('id'))
    elif datatype == 'D':
        c = Track.objects.filter(**args).values(alias).annotate(val = Avg('timelength'))
    else:
        c = Track.objects.filter(**args).values(alias).annotate(val = Count('id'))

    if save and c:
        for a in c:
            tg = TrackGroup()
            tg.grouptype = grouptype
            tg.groupcate = groupcate
            tg.groupdate = groupdate
            tg.datatype = datatype
            tg.name = a[alias]
            tg.count = int(a['val'])
            tg.dateline = endtime
            tg.save()
        print starttime, endtime, grouptype, datatype, groupcate, groupdate
    return c