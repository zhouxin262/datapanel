#coding=utf-8
import ast
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from project.models import Project
from session.models import Session
from track.models import Track
from datapanel.models import CmdSerialNumber
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
    e = datetime.now()
    s = datetime.now() - timedelta(seconds=60)
    html = 'django_session_count: %d' % DjangoSession.objects.filter().count()
    html += '<br/>project_count: %d' % Project.objects.filter().order_by('-id')[0].id
    html += '<br/>session_count: %d, increasing by %d/min' % (Session.objects.filter().order_by('-id')[0].id, Session.objects.filter(start_time__range=[s, e]).count())
    html += '<br/>track_count: %d, increasing by %d/min' % (Track.objects.filter().order_by('-id')[0].id, Track.objects.filter(dateline__range=[s, e]).count())
    # html += '<br/>swipe_count: %d' % Swipe.objects.filter().count()
    for cmdSerialNumber in CmdSerialNumber.objects.filter():
        html += '<br/>%s: %d of %s' % (cmdSerialNumber.name, cmdSerialNumber.last_id, cmdSerialNumber.class_name)
    return HttpResponse(html)


def get_or_create_session(request, project):
    # 客户服务器访问，可带客户的客户session_key
    session_key = None
    if request.GET.get('s', None):
        session_key = request.GET.get('s')
    else:
        session_key = request.session.session_key
    s = Session.objects.get_or_create(sn=session_key,
                                      project=project)
    if s[1]:
        s[0].ipaddress = request.META.get('REMOTE_ADDR', '0.0.0.0')
        s[0].set_user_agent(request.META.get('HTTP_USER_AGENT', ''))
        s[0].user_timezone = request.META.get('TZ', '')

        #try:
        params = ast.literal_eval(request.GET.get('p', ''))
        s[0].set_referrer(params['referrer'])
        # except:
        #     pass

        s[0].save()
    return s


def t(request):
    response = HttpResponse(mimetype="application/x-javascript")
    if not request.session.session_key:
        request.session.flush()
        request.session.save()

    token = request.GET.get('k', -1)
    project = Project.objects.get(token=token)

    # verify the url
    if request.META.get('HTTP_REFERER', '').find(project.url) == -1 and not request.GET.get('DEBUG'):
        return response

    s = get_or_create_session(request, project)

    if request.GET.get('t', ''):
        session = s[0]
        # filter actions
        try:
            prv_track = Track.objects.filter(session=session).order_by('-dateline')[0]
            if request.META.get('HTTP_REFERER', '') and prv_track.url == request.META.get('HTTP_REFERER', '') and prv_track.action == request.GET.get('t', ''):
                # f5 refresh
                return response
        except IndexError:
            prv_track = None

        # if action does not exist then add it
        action = session.project.add_action(request.GET.get('t', ''), request.META.get('HTTP_REFERER', ''))

        t = Track()
        t.project = session.project
        t.session = session
        t.action = action
        t.url = request.META.get('HTTP_REFERER', '')
        t.param = request.GET.get('p', '')
        t.dateline = now()
        t.save()

        t.set_from_track()
        add_timelength = t.set_prev_timelength()

        # add_track to update the cache data
        # add_track(t)

        session.track_count = session.track_count + 1
        if add_timelength > 0 and add_timelength <= 300:
            session.timelength += add_timelength
        session.save()

        # deal with param
        if t.param_display():
            for k, v in t.param_display().items():
                if len(k.split("__")) > 1:
                    getattr(t, k.split("__")[0]).set_value(k.split("__")[1], v)
                else:
                    if k.find('referrer') == -1:
                        t.set_value(k, v)
                    else:
                        t.set_referrer(v)

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
        response.write(response_data)
        return response
    return response
