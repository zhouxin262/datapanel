#coding=utf-8
import ast
import base64
from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from project.models import Project
from session.models import Session
from track.models import Track
from ecshop.models import OrderInfo, Goods
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
    return HttpResponse(html)


def a(request):
    response = HttpResponse(mimetype="application/x-javascript")
    return response


def analysis(request, response):
    if not request.GET.get('data'):
        # no data, give up
        return response
    try:
        # cannot decode, give up
        data = ast.literal_eval(base64.b64decode(request.GET.get('data')))
    except:
        return response

    if not data.has_key('a') or not data.has_key('k'):
        # donot know what to do
        return response

    todo = data['a']
    token = data['k']

    if todo == 'run':
        function_name = data['f']
        function_param = data['p']


        session = Session.objects.get(session_key=request.session[settings.TMP_SESSION_COOKIE_NAME])
        if not session.project:
            # update 'project' in session table
            session.project = Project.objects.get(token=token)
            session.save()

        # define const
        http_url = request.META.get('HTTP_REFERER', '')
        action_name = request.GET.get('t', '')
        params = request.GET.get('p', '')
        param_dic = {}
        try:
            param_dic = ast.literal_eval(params)
        except:
            pass
        # end define

        # verify the url
        if http_url.find(session.project.url) == -1 and not request.GET.get('DEBUG'):
            return response

        if action_name:
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
            http_referrer = ''
            if param_dic and param_dic['referrer']:
                http_referrer = param_dic['referrer']
                # set from track by referrer
            from_track = track.set_from_track(http_referrer)
            if not from_track.id == track.id:
                session.timelength += from_track.timelength
            session.save()

            # deal with param
            for k, v in param_dic.items():
                if len(k.split("__")) > 1:
                    getattr(track, k.split("__")[0]).set_value(k.split("__")[1], v)
                elif k.find('referrer') == -1 and k.find('function') == -1:
                        track.set_value(k, v)
                elif k.find('referrer') >= 0:
                    track.set_referrer(v)

        if param_dic and param_dic['function']:
            function_name = param_dic['function'][0]
            function_param = param_dic['function'][1]
            if function_name == 'ecs_order':
                function_param.update({"project": session.project, "session": session})
                OrderInfo.objects.process(**function_param)
            elif function_name == 'ecs_orderstatus':
                function_param.update({"project": session.project})
                OrderInfo.objects.process(**function_param)
            elif function_name == 'ecs_goods':
                function_param.update({"project": session.project})
                Goods.objects.process(**function_param)
            elif function_name == 'set_user':
                # todo: set user
                pass
    return response
