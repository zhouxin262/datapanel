#coding=utf8
from django.shortcuts import render


def overview(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    return render(request, 'ecshop/overview.html', {'project': project, })
