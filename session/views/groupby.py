#coding=utf-8
from datetime import datetime, timedelta

from django.db.models import Max, Sum, Count
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import redirect_to_login

from session.models import Session, SessionValue
from datapanel.utils import get_times


def referer(request, id, referer_attr):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    interval = int(request.GET.get('interval', 1))

    s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    e = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if interval == 30:
        s = s - timedelta(days=30)
    elif interval == 7:
        s = s - timedelta(days=7)
    elif interval == 1:
        s = s - timedelta(days=1)
    else:
        e = datetime.now()

    dataset = {}
    datalist = Session.objects.filter(start_time__range=[s, e]).values('user_referer_' + referer_attr).annotate(c=Count('id'), s=Sum('track_count')).order_by('c')
    for r in datalist:
        r['ec'] = round(float(r['s']) / (r['c']), 2)
        args = {'session__start_time__range': [s, e], 'name': 'success_1', 'session__user_referer_' + referer_attr: r['user_referer_' + referer_attr]}
        success_1 = SessionValue.objects.filter(**args).count()
        dataset[r['user_referer_' + referer_attr]] = {'label': r['user_referer_' + referer_attr], 'c': r['c'], 's': r['s'], 'ec': r['ec'], 'success_1': success_1}
    return render(request, 'session/groupby/referer.html', {'project': project,
                                                            'dataset': dataset, 'params': {'referer_attr': referer_attr, 'interval': interval}})
