# coding=utf8
from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.cache import cache_page

from datapanel.models import Timeline
from ecshop.models import Report1, Report2, OrderInfo


#@cache_page(60 * 5)
def overview(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    r = Report1.objects.cache(project)
    report = Report1.objects.filter(project=project, timeline__datetype='day').order_by('-timeline__dateline')
    len(report)  # or anything that will evaluate and hit the db
    report._result_cache.append(r)
    return render(request, 'ecshop/overview.html', {'project': project, 'report': report})


@cache_page(60 * 5)
def report2(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    s = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
    timeline = Timeline.objects.get_or_create(datetype='day', dateline=s)[0]
    report = Report2.objects.filter(project=project, timeline=timeline, sellcount__gt=0).order_by('-sellcount')
    return render(request, 'ecshop/report2.html', {'project': project, 'report': report})


def orderinfo(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    s = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
    e = request.GET.get('e', (datetime.strptime(s, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))

    drange = [s, e]
    orderlist = OrderInfo.objects.filter(project=project, add_dateline__range=drange)
    return render(request, 'ecshop/orderinfo.html', {'project': project, 'orderlist': orderlist})
