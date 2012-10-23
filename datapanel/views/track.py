#coding=utf8
import ast, time, md5
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from datapanel.utils import now, today_str
from datapanel.models import Project, Session, Track, Referer, TrackCondition, TrackGroupByClick, Action, TrackValue

@cache_page(60 * 5)
def list(request, id):
    project = request.user.participate_projects.get(id = id)

    value_names = cache.get(id + '_trackvalue_names', 'DoesNotExist')
    if value_names == 'DoesNotExist':
        value_names = TrackValue.objects.filter(track__session__project = project).distinct().values('name')
        cache.set(id + '_trackvalue_names', value_names)

    start_date = request.GET.get('start_date', today_str())
    end_date = request.GET.get('end_date', today_str())
    groupby = request.GET.get('groupby', 'referer')
    value = request.GET.get('value', 'action')

    querystr = 'start_date=%s&end_date=%s&groupby=%s&value=%s' % (start_date, end_date, groupby, value)
    params = {'start_date':start_date, 'end_date':end_date, 'groupby':groupby, 'value':value, 'querystr':querystr}
    args = {'track__session__project':project, 'name': groupby, 'value__isnull': False, 'track__dateline__gte':start_date, 'track__dateline__lte':end_date}

    tracks = TrackValue.objects.filter(**args).values('track__' + value, 'value').annotate(c = Count('value')).order_by('-c')

    paginator = Paginator(tracks, 25)
    page = request.GET.get('page')

    try:
        track_list = paginator.page(page)
    except PageNotAnInteger:
        track_list = paginator.page(1)
    except EmptyPage:
        track_list = paginator.page(paginator.num_pages)
    return render(request, 'datapanel/track/list.html', {'project':project,
        'value_names':value_names,
        'params':params,
        'track_list':track_list})


def get_or_create_session(request):
    token = request.GET.get('k', -1)
    # 客户服务器访问，可带客户的客户session_key
    session_key = None
    if request.GET.get('s', None):
        session_key = request.GET.get('s')
    else:
        session_key = request.session.session_key
    p = Project.objects.get(token = token)
    s = Session.objects.get_or_create(sn = session_key,
        project=p)
    if s[1]:
        s[0].ipaddress = request.META.get('REMOTE_ADDR','0.0.0.0')
        s[0].user_agent = request.META.get('HTTP_USER_AGENT','')
        s[0].user_timezone = request.META.get('TZ','')
        s[0].save()
    return s

def default(request):
    if not request.session.session_key:
        request.session.flush()
        request.session.save()

    s = get_or_create_session(request)

    if request.GET.get('t',''):
        session = s[0]
        # filter actions
        try:
            prv_track = Track.objects.filter(session = session).order_by('-dateline')[0]
            if  prv_track.url == request.META.get('HTTP_REFERER','') and prv_track.action == request.GET.get('t',''):
                # f5 refresh
                return HttpResponse('', mimetype="application/javascript")
        except IndexError:
            prv_track = None

        try:
            a = Action.objects.get(name = request.GET.get('t', ''))
        except Action.DoesNotExist:
            return HttpResponse('', mimetype="application/javascript")

        t = Track()
        t.session = session
        t.action = request.GET.get('t','')
        t.url = request.META.get('HTTP_REFERER','')
        t.param = request.GET.get('p','')
        t.dateline = now()
        t.set_times()
        # set step
        t.step = t.session.track_count + 1
        session.track_count = session.track_count + 1
        session.save()
        # todo : set timelength
        if prv_track:
            timelength = t.dateline - prv_track.dateline
            if timelength.seconds > 0 and timelength.seconds < 300:
                # 5min no move, definitely away from keyboard!
                prv_track.timelength = timelength.seconds
                prv_track.save()
        t.timelength = 0
        t.save()


        for datetype in ['hourline', 'dayline', 'weekline', 'monthline']:
            conditions = TrackCondition.objects.filter(project = session.project)
            for condition in conditions:
                test_result = condition.run_test(t)
                t.set_condition_result(condition, test_result)
                if test_result:
                    trackGroupByClick = TrackGroupByClick.objects.get_or_create(project = s[0].project, datetype=datetype, action=t.action, dateline=time.mktime(getattr(t, datetype).timetuple()), condition = condition)
                    trackGroupByClick[0].increase_value()

            trackGroupByClick = TrackGroupByClick.objects.get_or_create(project = s[0].project, datetype=datetype, action=t.action, dateline=time.mktime(getattr(t, datetype).timetuple()), condition=None)
            trackGroupByClick[0].increase_value()
        # deal with param
        if t.param_display():
            for k,v in t.param_display().items():
                t.set_value(k, v)

            # deal with referer
            if t.referer():
                r = Referer()
                r.session = session
                param = t.referer()
                r.site = param['referer_site']
                r.url = param['referer']
                if param.has_key('referer_keyword'):
                    r.keyword = param['referer_keyword']
                else:
                    r.keyword = ''
                r.save()

    if request.GET.get('p', ''):
        params = ast.literal_eval(request.GET.get('p', ''))
        if params.has_key('function') and params['function']:
            f = params['function']
            if f[0] == 'set_user':
                s[0].username = f[1]['username']
                s[0].save()

    if s[1]:
        # 新开的session，在客户服务器上存一个，需要配合
        response_data = 'jx.callback({mp_act:"set_session", mb_session_key: "%s"});' % s[0].sn;
        return HttpResponse(response_data, mimetype="application/javascript")
    return HttpResponse('', mimetype="application/javascript")