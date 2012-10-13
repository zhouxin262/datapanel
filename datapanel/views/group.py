#coding=utf-8
from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Count

from datapanel.utils import UTC
from datapanel.models import Track



def home(request, id):
    s = datetime.now()
    # deal with params 0.01
    project = request.user.participate_projects.get(id = id)
    grouptype = request.GET.get('grouptype','action')
    datatype = request.GET.get('datatype','click')
    groupcate = request.GET.get('groupcate','A')
    groupdate = request.GET.get('groupdate','dayline')
    interval = int(request.GET.get('interval',1))
    timeline = int(request.GET.get('timeline',0))
    params = {'grouptype':grouptype,'datatype':datatype,'groupcate':groupcate,'groupdate':groupdate,'interval':interval,'timeline':timeline}
    # deal with time range 0
    times = []
    if groupdate == 'hourline':
        for i in range(5):
            times.append(datetime.now(UTC()).replace(minute=0, second=0, microsecond=0) - timedelta(hours=i*interval + timeline))
    elif groupdate == 'dayline':
        for i in range(5):
            times.append(datetime.now(UTC()).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*interval + timeline))
    elif groupdate == 'weekline':
        for i in range(5):
            times.append(datetime.now(UTC()).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=datetime.now(UTC()).weekday()) - timedelta(days=7*i*interval + timeline*7))
    elif groupdate == 'monthline':
        for i in range(5):
            month = ( datetime.now(UTC()).month + i*interval + timeline ) % 12
            if month == 0:
                month = 12
            times.append(datetime.now(UTC()).replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0))
    # deal with actions 0.47
    args = {'session__project': project, }
    actions = [a['action'] for a in Track.objects.filter(**args).values(grouptype).distinct().order_by(grouptype)]
    args[groupdate + '__in'] = times
    args[grouptype + '__in'] = actions

    print datetime.now() - s
    s = datetime.now()
    ts = Track.objects.filter(**args).order_by(grouptype, '-' + groupdate).values(grouptype, groupdate).annotate(val = Count('id'))

    print datetime.now() - s
    s = datetime.now()
    # process data
    data = {}
    init_data = {}
    for t in times:
        init_data[t] = 0
    for a in actions:
        data[a] = init_data

    print datetime.now() - s
    s = datetime.now()
    for t in ts:
        data[t['action']][t[groupdate]] = t['val']

    print datetime.now() - s
    s = datetime.now()
    return render(request, 'datapanel/group/home.html', {'project':project,'params':params, 'times': times, 'data': data }) #'trackgroup_list': trackgroup_list,