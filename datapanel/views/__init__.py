#coding=utf-8
import ast

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from project.models import Project
from session.models import Session
from track.models import Track
from datapanel.utils import now


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


def get_or_create_session(request):
    token = request.GET.get('k', -1)
    # 客户服务器访问，可带客户的客户session_key
    session_key = None
    if request.GET.get('s', None):
        session_key = request.GET.get('s')
    else:
        session_key = request.session.session_key
    p = Project.objects.get(token=token)
    s = Session.objects.get_or_create(sn=session_key,
                                      project=p)
    if s[1]:
        s[0].ipaddress = request.META.get('REMOTE_ADDR', '0.0.0.0')
        s[0].user_agent = request.META.get('HTTP_USER_AGENT', '')
        s[0].user_timezone = request.META.get('TZ', '')
        s[0].save()
    return s


def t(request):
    if not request.session.session_key:
        request.session.flush()
        request.session.save()

    s = get_or_create_session(request)

    if request.GET.get('t', ''):
        session = s[0]
        # filter actions
        try:
            prv_track = Track.objects.filter(session=session).order_by('-dateline')[0]
            if prv_track.url == request.META.get('HTTP_REFERER', '') and prv_track.action == request.GET.get('t', ''):
                # f5 refresh
                return HttpResponse('', mimetype="application/javascript")
        except IndexError:
            prv_track = None

        t = Track()
        t.session = session
        t.action = request.GET.get('t', '')
        t.url = request.META.get('HTTP_REFERER', '')
        t.param = request.GET.get('p', '')
        t.dateline = now()
        t.save()

        session.track_count = session.track_count + 1
        session.save()

        session.project.add_action(t.action, t.url)

        # deal with param
        if t.param_display():
            for k, v in t.param_display().items():
                t.set_value(k, v)

    if request.GET.get('p', ''):
        params = ast.literal_eval(request.GET.get('p', ''))
        if 'function' in params and params['function']:
            f = params['function']
            if f[0] == 'set_user':
                s[0].username = f[1]['username']
                s[0].save()

    if s[1]:
        # 新开的session，在客户服务器上存一个，需要配合
        response_data = 'jx.callback({mp_act:"set_session", mb_session_key: "%s"});' % s[0].sn
        return HttpResponse(response_data, mimetype="application/javascript")
    return HttpResponse('', mimetype="application/javascript")
