#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login

from track.models import TrackValue


def get_referer_url(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    name = request.GET.get('name', '')
    value = request.GET.get('value', '')

    if name == 'referer_site':
        return HttpResponseRedirect('http://' + value)
    else:
        ts = TrackValue.objects.filter(track__session__project=project, name=name, value=value).order_by('-id')[:1]
        if ts:
            return HttpResponseRedirect(ts[0].track.get_value('referer'))
        else:
            return HttpResponse('403 forbidden')


def get_url_by_value(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    name = request.GET.get('name', '')
    value = request.GET.get('value', '')

    ts = TrackValue.objects.filter(track__session__project=project, name=name, value=value)[:1]
    if ts:
        return HttpResponseRedirect(ts[0].track.url)
    else:
        return HttpResponse('403 forbidden')
