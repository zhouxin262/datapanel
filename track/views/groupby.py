#coding=utf-8
import time
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.views import redirect_to_login

from track.models import TrackGroupByValue, TrackGroupByAction
from datapanel.utils import now


def referer(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    # deal with value_names
    value_names = [{"name": "referer_keyword"}, {"name": "referer_site"}]

    datetype = request.GET.get('datetype', 'day')
    name = request.GET.get('name', value_names[0]['name'])
    interval = int(request.GET.get('interval', 1))
    timeline = int(request.GET.get('timeline', 0))
    params = {'datetype': datetype, 'interval': interval, 'timeline':
              timeline, 'name': name}
    # deal with time range
    times = []

    if datetype == 'day':
        for i in range(7):
            t = now().replace(hour=0, minute=0, second=0,
                              microsecond=0) - timedelta(days=i * interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'week':
        for i in range(7):
            t = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now().weekday()) - timedelta(days=7 * i * interval + timeline * 7)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'month':
        for i in range(7):
            year = now().year - ((i * interval + timeline) / 12)
            month = (now().month - i * interval + timeline) % 12
            if month == 0:
                month = 12
            t = now().replace(year=year, month=month, day=1,
                              hour=0, minute=0, second=0, microsecond=0)
            times.append((t, int(time.mktime(t.timetuple()))))

    # deal with actions
    # actions = [a['value'] for a in TrackGroupByValue.objects.filter(project=project, name=name, value__isnull=False).values('value').distinct().order_by('value')]
    timestamps = [t[1] for t in times]
    args = {'project': project, 'datetype': datetype, 'name': name,
            'dateline__in': timestamps, 'count__gt': 20}
    trackGroupByValues = TrackGroupByValue.objects.filter(
        **args).exclude(value='').order_by('-dateline', '-count')

    # for the graph
    top10 = trackGroupByValues[:10]

    data = {}
    for trackGroupByValue in trackGroupByValues:
        if trackGroupByValue.value not in data:
            data[trackGroupByValue.value] = {'id': trackGroupByValue.id, 'label': trackGroupByValue.value, 'data': [(i, 0) for i in timestamps]}
        data[trackGroupByValue.value]['data'][timestamps.index(trackGroupByValue.dateline)] = ((trackGroupByValue.dateline, trackGroupByValue.count))
    return render(request, 'track/groupby_referer.html', {'project': project, 'params': params, 'times': times, 'value_names': value_names, 'data': data, 'top10': top10})


def value(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    # deal with value_names
    value_names = cache.get(id + '_trackvalue_names', 'DoesNotExist')
    if value_names == 'DoesNotExist':
        value_names = TrackGroupByValue.objects.filter(project=project).exclude(name__startswith='referer').distinct().values('name')
        cache.set(id + '_trackvalue_names', value_names)

    # todo: no value_names
    if not value_names:
        return HttpResponse('<a href="javascript:history.go(-1);">no data now</a>')
    datetype = request.GET.get('datetype', 'day')
    name = request.GET.get('name', value_names[0]['name'])
    interval = int(request.GET.get('interval', 1))
    timeline = int(request.GET.get('timeline', 0))
    params = {'datetype': datetype, 'interval': interval, 'timeline':
              timeline, 'name': name}
    # deal with time range
    times = []
    if datetype == 'hour':
        for i in range(7):
            t = now().replace(minute=0, second=0,
                              microsecond=0) - timedelta(hours=i * interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'day':
        for i in range(7):
            t = now().replace(hour=0, minute=0, second=0,
                              microsecond=0) - timedelta(days=i * interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'week':
        for i in range(7):
            t = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now().weekday()) - timedelta(days=7 * i * interval + timeline * 7)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'month':
        for i in range(7):
            year = now().year - ((i * interval + timeline) / 12)
            month = (now().month - i * interval + timeline) % 12
            if month == 0:
                month = 12
            t = now().replace(year=year, month=month, day=1,
                              hour=0, minute=0, second=0, microsecond=0)
            times.append((t, int(time.mktime(t.timetuple()))))

    # deal with actions
    # actions = [a['value'] for a in TrackGroupByValue.objects.filter(project=project, name=name, value__isnull=False).values('value').distinct().order_by('value')]
    timestamps = [t[1] for t in times]
    args = {'project': project, 'datetype': datetype, 'name': name,
            'dateline__in': timestamps, 'count__gt': 10}
    trackGroupByValues = TrackGroupByValue.objects.filter(
        **args).order_by('value', 'dateline')
    data = {}
    for trackGroupByValue in trackGroupByValues:
        if trackGroupByValue.value not in data:
            data[trackGroupByValue.value] = {'label':
                                             trackGroupByValue.value, 'data': [(i, 0) for i in timestamps]}
        data[trackGroupByValue.value]['data'][timestamps.index(trackGroupByValue.dateline)] = ((trackGroupByValue.dateline, trackGroupByValue.count))
    return render(request, 'track/groupby_value.html', {'project': project, 'params': params, 'times': times, 'value_names': value_names, 'data': data})


def action(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    # datetype = request.GET.get('datetype', 'day')
    # condition_id = int(request.GET.get('condition_id', 0))
    interval = int(request.GET.get('interval', 1))
    # timeline = int(request.GET.get('timeline', 0))
    # params = {'datetype': datetype, 'interval': interval, 'timeline':
    #           timeline, 'condition_id': condition_id}

    # deal with time range
    times = []
    datetype = 'hour'
    if interval == 1:
        datetype = 'hour'
        for i in range(24):
            t = now().replace(hour=0, minute=0, second=0,
                              microsecond=0) - timedelta(hours=i + 1)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif interval == 7 or interval == 30:
        datetype = 'day'
        for i in range(interval):
            t = now().replace(hour=0, minute=0, second=0,
                              microsecond=0) - timedelta(days=i + 1)
            times.append((t, int(time.mktime(t.timetuple()))))

    # deal with actions
    actions = [a.name for a in project.action.filter().order_by('name')]

    times = times[::-1]
    timestamps = [t[1] for t in times]
    args = {'project': project, 'datetype': datetype, 'dateline__in':
            timestamps}
    # if condition_id == 0:
    #     args['condition__isnull'] = True
    # else:
    #     args['condition_id'] = condition_id

    data = {}
    for action in actions:
        data[action] = {'label': action, 'data': [(i, 0) for i in timestamps]}

    for trackGroupByAction in TrackGroupByAction.objects.filter(**args).order_by('action', 'dateline'):
        data[trackGroupByAction.action.name]['data'][timestamps.index(trackGroupByAction.dateline)] = ((trackGroupByAction.dateline, trackGroupByAction.count))

    # # deal with conditions
    # conditions = TrackCondition.objects.filter(project=project)
    params = {'interval': interval, 'datetype':datetype }
    return render(request, 'track/groupby_track.html', {'project': project, 'params': params, 'times': times, 'actions': actions, 'data': data})
