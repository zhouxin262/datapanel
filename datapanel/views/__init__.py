# coding=utf-8
import ast
import base64
import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from project.models import Project
from session.models import Session
from track.models import Track
from datapanel.utils import now, RunFunctions

logger = logging.getLogger(__name__)


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
    html = 'django_session_count: %d, increasing by %d/min' % (
        DjangoSession.objects.filter().count(), DjangoSession.objects.filter(expire_date__range=[es, ee]).count())
    html += '<br/>project_count: %d' % Project.objects.filter().order_by('-id')[0].id
    html += '<br/>session_count: %d, increasing by %d/min' % (
        Session.objects.filter().order_by('-id')[0].id, Session.objects.filter(start_time__range=[s, e]).count())
    html += '<br/>track_count: %d, increasing by %d/min' % (
        Track.objects.filter().order_by('-id')[0].id, Track.objects.filter(dateline__range=[s, e]).count())
    # html += '<br/>swipe_count: %d' % Swipe.objects.filter().count()
    return HttpResponse(html)


def a(request):
    response = HttpResponse(mimetype="application/x-javascript")
    return response


def dict_string_unquote(dic):
    import urllib2
    for k, v in dic.items():
        if type(v) == str:
            dic[k] = urllib2.unquote(v).decode('utf-8')
        elif type(v) == dict:
            dic[k] = dict_string_unquote(v)
        else:
            dic[k] = v
    return dic


def get_and_verify_data(request):
    """(bool:verified, dict:data)"""
    data = None
    is_verified = True

    if 'data' in request.GET:
        try:
            data = ast.literal_eval(base64.b64decode(request.GET.get('data')))
            data = dict_string_unquote(data)
        except:
            logger.debug(request.GET.get('data'))
            is_verified = False

        if not data or 'k' not in data or 'u' not in data or 'r' not in data or 'a' not in data:
            is_verified = False
        else:
            todo = data.get('a')
            if (todo == 'run' and 'f' not in data) or (todo == 'track' and 'e' not in data):
                is_verified = False
    else:
        is_verified = False
    # todo: verify the url

    return (is_verified, data)


def analysis(request, response):
    (is_verified, data) = get_and_verify_data(request)
    if not is_verified:
        return response

    todo = data.get('a')
    token = data.get('k')

    # set session and project
    session = Session.objects.get(session_key=request.session[settings.TMP_SESSION_COOKIE_NAME])
    if not session.project:
        # update 'project' in session table
        session.project = Project.objects.get(token=token)
        session.save()
    if todo == 'run':
        func = data.get('f')
        param = data.get('p', None)
        f = RunFunctions()
        param.update({'session': session, 'project': session.project})
        getattr(f, func)(param)

    elif todo == 'track':
        # define const
        http_url = data.get('u')
        action_name = data.get('e')
        referrer = data.get('r')
        param_dic = data.get('p', {})

        # if action does not exist then add it
        action = session.project.add_action(action_name, http_url)

        track = Track()
        track.project = session.project
        track.session = session
        track.action = action
        track.url = http_url
        track.dateline = now()
        track.save()
        session.track_count = session.track_count + 1

        # set from track by referrer
        from_track = track.set_from_track(referrer)
        if not from_track.id == track.id:
            session.timelength += from_track.timelength
        session.save()

        # set referrer
        track.set_referrer(referrer)

        # deal with param
        for k, v in param_dic.items():
            if len(k.split("__")) > 1:
                getattr(track, k.split("__")[0]).set_value(k.split("__")[1], v)
            else:
                track.set_value(k, v)
    return response
