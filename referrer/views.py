#coding=utf-8
from datetime import datetime, timedelta

from django.db.models import Sum
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

    args = {'dateline__range': [s, e], 'datetype': 'day'}
    dbtable = GReferrerKeyword
    dataset = []
    if referrer_attr == "site":
        dbtable = GReferrerSite

    for datarow in dbtable.objects.filter(**args).values('user_referrer_' + referrer_attr).annotate(count=Sum('count'), track_count=Sum('track_count'), timelength=Sum('timelength')):
        dataset.append({"label": datarow['user_referrer_' + referrer_attr],
                        "datarow": datarow,
                        "avg_track_count": round(float(datarow["track_count"]) / datarow["count"], 2),
                        "avg_timelength": round(float(datarow["timelength"]) / datarow["count"], 2)})
    return render(request, 'referrer/session.html', {'project': project,
                                                     'dataset': dataset, 'params': {'referrer_attr': referrer_attr, 'interval': interval, 'page': page}})
