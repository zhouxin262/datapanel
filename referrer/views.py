#coding=utf-8
from datetime import datetime, timedelta

from django.db.models import Sum, Avg
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login

from session.models import GReferrerSite, GReferrerKeyword


def session(request, id, referrer_attr):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    interval = int(request.GET.get('interval', 1))
    page = int(request.GET.get('page', 1))

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

    args = {'timeline__dateline__range': [s, e], 'timeline__datetype': 'day'}
    dbtable = GReferrerKeyword
    dataset = []
    if referrer_attr == "site":
        dbtable = GReferrerSite

    tmp = dbtable.objects.filter(**args).exclude(**{'referrer_' + referrer_attr + '__name': ''}).values('referrer_' + referrer_attr + '__name').values(
        'referrer_' + referrer_attr + '__name').annotate(
            count=Sum('count'),
            track_count=Avg('track_count'),
            timelength=Avg('timelength'),
        ).order_by('-count')
    for datarow in tmp:
        datarow['timelength_display'] = "%d分%d秒" % (datarow['timelength'] / 60, datarow['timelength'] % 60)
        dataset.append({"label": datarow['referrer_' + referrer_attr + '__name'],
                        "datarow": datarow})
    return render(request, 'referrer/session.html', {'project': project,
                                                     'dataset': dataset, 'params': {'referrer_attr': referrer_attr, 'interval': interval, 'page': page}})
