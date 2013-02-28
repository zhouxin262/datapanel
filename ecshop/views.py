# coding=utf8
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.cache import cache_page

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
def report2(request, id, timeline_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    report = Report2.objects.filter(project=project, timeline__id=timeline_id).order_by('-sellcount')
    return render(request, 'ecshop/report2.html', {'project': project, 'report': report})


def orderinfo(request, id):
    from datetime import datetime, timedelta

    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    start_dateline = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
    end_dateline = request.GET.get(
        'e', (datetime.strptime(start_dateline, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))

    drange = [start_dateline, end_dateline]
    orderlist = OrderInfo.objects.filter(project=project, add_dateline__range=drange)
    return render(request, 'ecshop/orderinfo.html', {'project': project, 'orderlist': orderlist})
