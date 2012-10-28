#coding=utf-8
import ast, time, md5
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.core import serializers
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import redirect_to_login

from datapanel.utils import now, today_str
from datapanel.models import Project, Session, Track, Referer, TrackCondition, TrackGroupByCondition, Action, TrackValue, TrackGroupByValue

@cache_page(60 * 5)
def groupby_value(request, id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    # deal with value_names
    value_names = cache.get(id + '_trackvalue_names', 'DoesNotExist')
    if value_names == 'DoesNotExist':
        value_names = TrackGroupByValue.objects.filter(project = project).distinct().values('name')
        cache.set(id + '_trackvalue_names', value_names)

    datetype = request.GET.get('datetype','day')
    name = request.GET.get('name', value_names[0]['name'])
    interval = int(request.GET.get('interval',1))
    timeline = int(request.GET.get('timeline',0))
    params = {'datetype':datetype,'interval':interval,'timeline':timeline,'name':name}
    # deal with time range
    times = []
    if datetype == 'hour':
        for i in range(7):
            t = now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=i*interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'day':
        for i in range(7):
            t = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'week':
        for i in range(7):
            t = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now().weekday()) - timedelta(days=7*i*interval + timeline*7)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'month':
        for i in range(7):
            year = now().year - ((i*interval + timeline) / 12)
            month = (now().month - i*interval + timeline ) % 12
            if month == 0:
                month = 12
            t= now().replace(year= year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
            times.append((t, int(time.mktime(t.timetuple()))))

    # deal with actions
    actions = [a['value'] for a in TrackGroupByValue.objects.filter(project=project, name=name, value__isnull=False).values('value').distinct().order_by('value')]
    args = {'project': project, 'datetype': datetype + 'line', 'name': name}

    data = []
    for i, action in enumerate(actions):
        print action
        data.append({'label': action, 'data': []})
        for j, t in enumerate(times):
            try:
                args.update({'value':action, 'dateline': t[1]})
                data[i]['data'].append((t[1], TrackGroupByValue.objects.get(**args).count))
            except TrackGroupByValue.DoesNotExist :
                data[i]['data'].append((t[1], 0))
    # process data
    return render(request, 'datapanel/track/groupby_value.html', {'project':project,'params':params,'times': times,'actions':actions,'value_names':value_names, 'data': data })

def get_url_by_value(request, id, name, value):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    ts = TrackValue.objects.filter(track__session__project = project, name = name, value = value)[:1]
    if ts:
        return HttpResponseRedirect(ts[0].track.url)



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
        # set timelength
        if prv_track:
            timelength = t.dateline - prv_track.dateline
            if timelength.seconds < 900:
                # 15min no move, definitely away from keyboard!
                prv_track.timelength = timelength.seconds + 1
                prv_track.save()
        t.timelength = 0
        t.save()

        # deal with param
        if t.param_display():
            for k,v in t.param_display().items():
                if k not in ('referer', ):
                    t.set_value(k, v)

        for datetype in ['hourline', 'dayline', 'weekline', 'monthline']:
            if t.param_display():
                for k,v in t.param_display().items():
                    if k not in ('referer', ):
                        trackGroupByValue = TrackGroupByValue.objects.get_or_create(project = s[0].project, datetype=datetype, name=k, value=v, dateline=time.mktime(getattr(t, datetype).timetuple()))
                        trackGroupByValue[0].increase_value()

            conditions = TrackCondition.objects.filter(project = session.project)
            for condition in conditions:
                test_result = condition.run_test(t)
                t.set_condition_result(condition, test_result)
                if test_result:
                    tg = TrackGroupByCondition.objects.get_or_create(project = s[0].project, datetype=datetype, action=t.action, dateline=time.mktime(getattr(t, datetype).timetuple()), condition = condition)
                    tg[0].increase_value()

            tg = TrackGroupByCondition.objects.get_or_create(project = s[0].project, datetype=datetype, action=t.action, dateline=time.mktime(getattr(t, datetype).timetuple()), condition=None)
            tg[0].increase_value()

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
