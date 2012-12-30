#coding=utf-8
import ast
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings

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
    ee = e + timedelta(days=365)
    es = s + timedelta(days=365)
    html = 'django_session_count: %d, increasing by %d/min' % (DjangoSession.objects.filter().count(), DjangoSession.objects.filter(expire_date__range=[es, ee]).count())
    html += '<br/>project_count: %d' % Project.objects.filter().order_by('-id')[0].id
    html += '<br/>session_count: %d, increasing by %d/min' % (Session.objects.filter().order_by('-id')[0].id, Session.objects.filter(start_time__range=[s, e]).count())
    html += '<br/>track_count: %d, increasing by %d/min' % (Track.objects.filter().order_by('-id')[0].id, Track.objects.filter(dateline__range=[s, e]).count())
    # html += '<br/>swipe_count: %d' % Swipe.objects.filter().count()
    for cmdSerialNumber in CmdSerialNumber.objects.filter():
        html += '<br/>%s: %d of %s' % (cmdSerialNumber.name, cmdSerialNumber.last_id, cmdSerialNumber.class_name)
    return HttpResponse(html)


def t(request):
    return HttpResponse('fuck')
    response = HttpResponse(mimetype="application/x-javascript")
    session = Session.objects.get(session_key=request.session[settings.TMP_SESSION_COOKIE_NAME])

    print 11, request.session.session_key
    # verify the url
    if request.META.get('HTTP_REFERER', '').find(session.project.url) == -1 and not request.GET.get('DEBUG'):
        return response

    if request.GET.get('t', ''):
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

        add_timelength = t.set_prev_timelength()

        # add_track to update the cache data
        # add_track(t)

        session.track_count = session.track_count + 1
        if add_timelength > 0 and add_timelength <= 300:
            session.timelength += add_timelength
        session.save()

        # deal with param
        if t.param_display():
            # set from track by referrer
            t.set_from_track(t.param_display()['referrer'])
            # set params
            for k, v in t.param_display().items():
                if len(k.split("__")) > 1:
                    getattr(t, k.split("__")[0]).set_value(k.split("__")[1], v)
                else:
                    if k.find('referrer') == -1 and k.find('function') == -1:
                        t.set_value(k, v)
                    elif k.find('referrer') >= 0:
                        t.set_referrer(v)
                    elif k.find('function') >= 0:
                        function_name = v[0]
                        function_param = v[1]
                        if function_name == 'set_user':
                            pass
                        elif function_name == 'ecs_order':
                            from ecshop.models import OrderInfo
                            function_param.update({"project": session.project, "session": session})
                            OrderInfo.objects.process(**function_param)

    print 22, request.session.session_key
    return response
