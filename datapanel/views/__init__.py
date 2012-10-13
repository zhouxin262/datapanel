#coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datapanel.models import Session, Track, Project

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))
    if not request.user.participate_projects.all():
        return HttpResponseRedirect(reverse('project_create'))
    else:
        lastview = request.user.participate_projects.order_by('-lastview')[0]
        return HttpResponseRedirect(reverse('project_home', args=[lastview.id]))

def server_info(request):
    from django.contrib.sessions.models import Session as DjangoSession
    html = 'django_session_count: %d' % DjangoSession.objects.filter().count()
    html += '<br/>project_count: %d' % Project.objects.filter().count()
    html += '<br/>session_count: %d' % Session.objects.filter().count()
    html += '<br/>track_count: %d' % Track.objects.filter().count()
    return HttpResponse(html)