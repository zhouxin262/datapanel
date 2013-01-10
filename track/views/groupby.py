#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
# from django.core.cache import cache
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.cache import cache_page

from track.models import GAction
from datapanel.utils import get_times


# def value(request, id):
#     try:
#         project = request.user.participate_projects.get(id=id)
#     except AttributeError:
#         return redirect_to_login(request.get_full_path())

#     # deal with value_names
#     # value_names = cache.get(id + '_trackvalue_names', 'DoesNotExist')
#     # if value_names == 'DoesNotExist':
#     value_names = GValue.objects.filter(project=project).exclude(name__startswith='referrer').distinct().values('name')
#     # cache.set(id + '_trackvalue_names', value_names)

#     # todo: no value_names
#     if not value_names:
#         return HttpResponse('<a href="javascript:history.go(-1);">no data now</a>')

#     interval = int(request.GET.get('interval', 1))
#     name = request.GET.get('name', value_names[0]['name'])

#     # deal with time range
#     (datetype, times) = get_times(interval)

#     # deal with actions
#     # actions = [a['value'] for a in GValue.objects.filter(project=project, name=name, value__isnull=False).values('value').distinct().order_by('value')]

#     args = {'project': project, 'datetype': datetype, 'name': name,
#             'dateline__in': times, 'count__gt': 10}
#     print int(2400 / interval) * interval
#     trackGroupByValues = GValue.objects.filter(**args).order_by('value', 'dateline')
#     data = {}
#     for trackGroupByValue in trackGroupByValues:
#         if trackGroupByValue.value not in data:
#             data[trackGroupByValue.value] = {'label':
#                                              trackGroupByValue.value, 'data': [(i, 0) for i in times]}
#         data[trackGroupByValue.value]['data'][times.index(trackGroupByValue.dateline)] = ((trackGroupByValue.dateline, trackGroupByValue.count))

#     params = {'interval': interval, 'datetype': datetype, 'name': name}
#     return render(request, 'track/groupby_value.html', {'project': project, 'params': params, 'times': times, 'value_names': value_names, 'data': data})


@cache_page(60 * 60 * 24)
def action(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    interval = int(request.GET.get('interval', 1))

    # deal with time range
    (datetype, times) = get_times(interval)

    # deal with actions
    actions = [a.name for a in project.action.filter().order_by('name')]

    times = times[::-1]
    args = {'project': project, 'timeline__datetype': datetype, 'timeline__dateline__in': times}

    data = {}
    for action in actions:
        data[action] = {'label': action, 'data': [(i, 0) for i in times]}

    for trackGroupByAction in GAction.objects.filter(**args).order_by('action', 'timeline__dateline'):
        data[trackGroupByAction.action.name]['data'][times.index(trackGroupByAction.timeline.dateline)] = ((trackGroupByAction.timeline.dateline, trackGroupByAction.count))

    params = {'interval': interval, 'datetype': datetype}
    return render(request, 'track/groupby_action.html', {'project': project, 'params': params, 'times': times, 'actions': actions, 'data': data})
