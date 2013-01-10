#coding=utf8
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.cache import cache_page

from ecshop.models import Report1, Report2


@cache_page(60 * 60 * 24)
def overview(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    report = Report1.objects.filter(timeline__datetype='day').order_by('-timeline__dateline')

    return render(request, 'ecshop/overview.html', {'project': project, 'report': report})


@cache_page(60 * 60 * 24)
def report2(request, id, timeline_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    report = Report2.objects.filter(timeline__id=timeline_id).order_by('-sellcount')

    return render(request, 'ecshop/report2.html', {'project': project, 'report': report})
    return render(request, 'ecshop/report2.html', {'project': project, 'report': report})
