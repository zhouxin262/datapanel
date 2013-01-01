#coding=utf-8
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from project.models import Project
from session.models import Session
from track.models import Track


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
    e = datetime.now()
    s = datetime.now() - timedelta(seconds=60)
    ee = e + timedelta(days=365)
    es = s + timedelta(days=365)
    html = 'django_session_count: %d, increasing by %d/min' % (DjangoSession.objects.filter().count(), DjangoSession.objects.filter(expire_date__range=[es, ee]).count())
    html += '<br/>project_count: %d' % Project.objects.filter().order_by('-id')[0].id
    html += '<br/>session_count: %d, increasing by %d/min' % (Session.objects.filter().order_by('-id')[0].id, Session.objects.filter(start_time__range=[s, e]).count())
    html += '<br/>track_count: %d, increasing by %d/min' % (Track.objects.filter().order_by('-id')[0].id, Track.objects.filter(dateline__range=[s, e]).count())
    # html += '<br/>swipe_count: %d' % Swipe.objects.filter().count()
    return HttpResponse(html)


def t(request):
    response = HttpResponse(mimetype="application/x-javascript")
    return response
