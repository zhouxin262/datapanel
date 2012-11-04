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


    datalist = TrackValue.objects.filter(name = 'referer_keyword').exclude(value=' ').values('value').annotate(s = Sum('track__session__track_count'), c=Count('track__session'))
    for r in datalist:
        r['e'] = float(r['s'])/float(r['c'])
    return render(request, 'session/groupby/referer.html', {'project': project,
                                                          'datalist': datalist})
