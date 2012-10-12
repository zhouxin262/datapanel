#coding=utf-8
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('auth_login'))
    if not request.user.participate_projects.all():
        return HttpResponseRedirect(reverse('project_create'))
    else:
        lastview = request.user.participate_projects.order_by('-lastview')[0]
        return HttpResponseRedirect(reverse('project_home', args=[lastview.id]))

def server_info(request):
    html = '<a href="/">点</a>'
    if request.GET.get('whois') == 'zx':
        from django.contrib.sessions.models import Session as DjangoSession
        html = 'django_session_count: %d' % DjangoSession.objects.filter().count()
        html += '<br/>session_count: %d' % Session.objects.filter().count()
        html += '<br/>track_count: %d' % Track.objects.filter().count()
        html += '<br/>trackgroup_count: %d' % TrackGroup.objects.filter().count()
    return HttpResponse(html)