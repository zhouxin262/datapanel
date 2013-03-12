# coding=utf-8
import json
from datetime import datetime, timedelta

from django.db.models import Sum, Avg
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.cache import cache_page

from session.models import Session, SessionArch, GReferrerSite, GReferrerKeyword
from ecshop.models import OrderInfo


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


@cache_page(60 * 15)
def order_keyword(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    s = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
    e = request.GET.get('e', (datetime.strptime(s, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))

    sessions = [o.session_id for o in OrderInfo.objects.filter(project=project, order_status__in=[1, 3, 5],
                                                               dateline__range=[s, e])]

    kws = {}
    ss = Session.objects.filter(id__in=sessions)
    len(ss)  # or anything that will evaluate and hit the db
    ss._result_cache.extend(SessionArch.objects.filter(id__in=sessions))
    for obj in ss:
        if obj.referrer_keyword:
            if obj.referrer_keyword.name in kws:
                kws[obj.referrer_keyword.name] += 1
            else:
                kws[obj.referrer_keyword.name] = 1
        if "" in kws:
            kws[""] += 1
        else:
            kws[""] = 1

    res = {"aaData": []}
    for k, v in kws.items():
        res["aaData"].append([k, v])

    if request.is_ajax():
        return render(request, 'datapanel/respond.json', {'res': json.dumps(res)}, content_type="application/json")

    return render(request, 'referrer/order_keyword.html', {'project': project, 'res': json.dumps(res)})


@cache_page(60 * 15)
def order_site(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    s = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
    e = request.GET.get('e', (datetime.strptime(s, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))

    sessions = [o.session_id for o in OrderInfo.objects.filter(project=project, order_status__in=[1, 3, 5],
                                                               dateline__range=[s, e])]

    kws = {}
    for sid in sessions:
        s = None
        try:
            s = Session.objects.get(id=sid)
        except Session.DoesNotExist:
            s = SessionArch.objects.get(id=sid)
        if s and s.referrer_site:
            if s.referrer_site.name in kws:
                kws[s.referrer_site.name] += 1
            else:
                kws[s.referrer_site.name] = 1
    return render(request, 'referrer/order_site.html', {'project': project, 'kws': kws})
