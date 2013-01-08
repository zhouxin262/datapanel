#coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.conf import settings

from track.models import Track, TrackValue
from session.models import Session
from project.models import Project
from datapanel.utils import now


def track(request, response):
    session = Session.objects.get(session_key=request.session[settings.TMP_SESSION_COOKIE_NAME])
    if not session.project and request.GET.get('k', None):
        token = request.GET.get('k', None)
        session.project = Project.objects.get(token=token)
        session.save()

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
