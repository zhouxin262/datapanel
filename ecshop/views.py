#coding=utf8
from django.shortcuts import render
from django.contrib.auth.views import redirect_to_login

from ecshop.models import Report1


def overview(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    report = Report1.objects.filter(datetype='day').order_by('-dateline')

    return render(request, 'ecshop/overview.html', {'project': project, 'report': report})
