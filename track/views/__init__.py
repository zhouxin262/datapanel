#coding=utf-8
import ast

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.conf import settings

from track.models import Track, TrackValue
from session.models import Session
from project.models import Project
from datapanel.utils import now


def track(request, response):
    session = Session.objects.get(session_key=request.session[settings.TMP_SESSION_COOKIE_NAME])
    if not session.project:
        if request.GET.get('k', None):
            # update 'project' in session table
            session.project = Project.objects.get(token=request.GET.get('k', None))
            session.save()
        else:
            return response

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
        if function_name == 'set_user':
            # todo: set user
            pass
        elif function_name == 'ecs_order':
            from ecshop.models import OrderInfo
            function_param.update({"project": session.project, "session": session})
            OrderInfo.objects.process(**function_param)
        elif function_name == 'ecs_goods':
            from ecshop.models import Goods
            function_param.update({"project": session.project})
            Goods.objects.process(**function_param)
    return response


def get_referrer_url(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    name = request.GET.get('name', '')
    value = request.GET.get('value', '')

    if name == 'referrer_site':
        return HttpResponseRedirect('http://' + value)
    else:
        ts = TrackValue.objects.filter(track__session__project=project, name=name, value=value).order_by('-id')[:1]
        if ts:
            return HttpResponseRedirect(ts[0].track.get_value('referrer'))
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
