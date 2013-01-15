#coding=utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.cache import cache_page

from ecshop.models import Report1, Report2, OrderInfo


def set_order_status(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    order_sn = request.GET.get('order_sn')
    status = request.GET.get('status')
    try:
        status = int(status)
    except:
        status = 0

    try:
        order = OrderInfo.objectss.get(order_sn=order_sn)
        order.status = status
        order.save()
        return HttpResponse('order update success')
    except OrderInfo.DoesNotExist:
        return HttpResponse('order does not exist')



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
