#coding=utf-8
import time
from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Count
from django.core import serializers

from datapanel.utils import UTC
from datapanel.models import TrackGroupByClick

def home(request, id):
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
            t = datetime.now(UTC()).replace(minute=0, second=0, microsecond=0) - timedelta(hours=i*interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif groupdate == 'dayline':
        for i in range(5):
            t = datetime.now(UTC()).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif groupdate == 'weekline':
        for i in range(5):
            t = datetime.now(UTC()).replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=datetime.now(UTC()).weekday()) - timedelta(days=7*i*interval + timeline*7)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif groupdate == 'monthline':
        for i in range(5):
            month = (datetime.now(UTC()).month + i*interval + timeline ) % 12
            if month == 0:
                month = 12
            t= datetime.now(UTC()).replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
            times.append((t, int(time.mktime(t.timetuple()))))

    # deal with actions 0.47
    args = {'project': project, 'dateline__in': [t[1] for t in times], 'datetype': groupdate}
    actions = [a['action'] for a in TrackGroupByClick.objects.filter().values(grouptype).distinct().order_by(grouptype)]
    data = serializers.serialize("json",TrackGroupByClick.objects.filter(**args), fields=('action','dateline','value'))

    # process data
    return render(request, 'datapanel/group/home.html', {'project':project,'params':params, 'times': times, 'actions':actions, 'data': data }) #'trackgroup_list': trackgroup_list,