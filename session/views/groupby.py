#coding=utf-8
from django.db.models import Max, Sum, Count
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import redirect_to_login

from track.models import TrackValue


def referer(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    name = request.GET.get('name', 'referer_keyword')

    datalist = TrackValue.objects.filter(name = name).exclude(value=' ').exclude(track__timelength__gte='1800').values('value').annotate(s = Sum('track__session__track_count'), t=Sum('track__timelength'), c=Count('track__session')).filter(c__gt=3)
    for r in datalist:
        r['ec'] = round(float(r['s'])/(r['c']), 2)
        r['et'] = round(float(r['t'])/(r['c']), 2)
    return render(request, 'session/groupby/referer.html', {'project': project,
                                                          'datalist': datalist, 'params': {'name' : name}})
