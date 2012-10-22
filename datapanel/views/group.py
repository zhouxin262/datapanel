#coding=utf-8
import time
from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Count
from django.core import serializers

from datapanel.utils import now
from datapanel.models import TrackGroupByClick, TrackCondition

def home(request, id):
    # deal with params
    project = request.user.participate_projects.get(id = id)
    datetype = request.GET.get('datetype','dayline')
    condition_id = int(request.GET.get('condition_id',0))
    interval = int(request.GET.get('interval',1))
    timeline = int(request.GET.get('timeline',0))
    params = {'datetype':datetype,'interval':interval,'timeline':timeline,'condition_id':condition_id}

    # deal with time range
    times = []
    if datetype == 'hourline':
        for i in range(5):
            t = now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=i*interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'dayline':
        for i in range(5):
            t = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*interval + timeline)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'weekline':
        for i in range(5):
            t = now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now().weekday()) - timedelta(days=7*i*interval + timeline*7)
            times.append((t, int(time.mktime(t.timetuple()))))
    elif datetype == 'monthline':
        for i in range(5):
            month = (now().month + i*interval + timeline ) % 12
            if month == 0:
                month = 12
            t= now().replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
            times.append((t, int(time.mktime(t.timetuple()))))

    # deal with actions
    actions = [a['action'] for a in TrackGroupByClick.objects.filter(project=project).values('action').distinct().order_by('action')]
    # deal with conditions
    conditions = TrackCondition.objects.filter(project=project)
    args = {'project': project, 'dateline__in': [t[1] for t in times], 'datetype': datetype}
    if condition_id == 0:
        args['condition__isnull'] = True
    else:
        args['condition_id'] = condition_id
    data = serializers.serialize("json",TrackGroupByClick.objects.filter(**args), fields=('action','dateline','value'))

    # process data
    return render(request, 'datapanel/group/home.html', {'project':project,'params':params,'times': times,'actions':actions,'conditions':conditions, 'data': data })

# def action(request, id):
#     # deal with action
#     project = request.user.participate_projects.get(id = id)
#     args = {'session__project': project, groupby +'__contains': keyword}

#     referers = Referer.objects.filter(**args).exclude(**{groupby:""}).values(groupby).annotate(c = Count('id')).order_by('-c')
#     paginator = Paginator(referers, 25)
#     page = request.GET.get('page')
#     try:
#         referer_list = paginator.page(page)
#     except PageNotAnInteger:
#         referer_list = paginator.page(1)
#     except EmptyPage:
#         referer_list = paginator.page(paginator.num_pages)
#     return render(request, 'datapanel/stream/referer_list.html', {'project':project, 'referer_list':referer_list,'params':params})