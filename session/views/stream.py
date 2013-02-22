# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse

from session.models import SessionValue, Session, SessionArch


def list(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    #过滤
    track_count__gt = int(request.GET.get('track_count__gt', 3))
    project_sessions = project.session_set.filter(track_count__gt=track_count__gt)

    #排序
    order = request.GET.get('order', 't')
    if order == 'c':
        project_sessions = project_sessions.order_by('-track_count')
    else:
        project_sessions = project_sessions.order_by('-id')

    querystr = 'track_count__gt=%d&order=%s' % (track_count__gt, order)
    params = {'order': order, 'track_count__gt': track_count__gt, 'querystr': querystr}

    paginator = Paginator(project_sessions, 15)
    page = request.GET.get('page')
    try:
        session_list = paginator.page(page)
    except PageNotAnInteger:
        session_list = paginator.page(1)
    except EmptyPage:
        session_list = paginator.page(paginator.num_pages)
    return render(request, 'session/stream/list.html', {'project': project,
                                                        'session_list': session_list, 'params': params})


def tile(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    #过滤
    track_count__gt = int(request.GET.get('track_count__gt', 3))
    project_sessions = project.session_set.filter(track_count__gt=track_count__gt)

    #排序
    order = request.GET.get('order', 't')
    if order == 'c':
        project_sessions = project_sessions.order_by('-track_count')
    else:
        project_sessions = project_sessions.order_by('-id')

    querystr = 'track_count__gt=%d&order=%s' % (track_count__gt, order)
    params = {'order': order, 'track_count__gt': track_count__gt, 'querystr': querystr}

    paginator = Paginator(project_sessions, 15)
    page = request.GET.get('page')
    try:
        session_list = paginator.page(page)
    except PageNotAnInteger:
        session_list = paginator.page(1)
    except EmptyPage:
        session_list = paginator.page(paginator.num_pages)

    return render(request, 'session/stream/tile.html', {'project': project,
                                                        'session_list': session_list, 'params': params})


def view(request, id, sid):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    try:
        session = Session.objects.get(id=sid)
        tracks = session.track_set.all().order_by('dateline')
    except:
        session = SessionArch.objects.get(id=sid)
        tracks = session.trackarch_set.all().order_by('dateline')


    paginator = Paginator(tracks, 20)
    page = request.GET.get('page')
    try:
        track_flow = paginator.page(page)
    except PageNotAnInteger:
        track_flow = paginator.page(1)
    except EmptyPage:
        track_flow = paginator.page(paginator.num_pages)
    return render(request, 'session/stream/view.html', {'project': project, 'track_flow': track_flow})


def get_stream_by_value(request, id):
    # todo
    # get stream by order SN
    # it does not belong here, should move into ecshop
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    name = request.GET.get('name', '')
    value = request.GET.get('value', '')

    session_id = 0
    if name == 'order_sn':
        from ecshop.models import OrderInfo
        try:
            session_id = OrderInfo.objects.get(order_sn=value).session_id
        except:
            pass
    else:
        ts = SessionValue.objects.filter(session__project=project, name=name, value__icontains=value).values('session')
        # todo list
        if len(ts) == 1:
            session_id = ts[0]['session']
        elif len(ts) > 1:
            session_id = ts[0]['session']

    if not session_id:
        return HttpResponse('403 forbidden')
    return HttpResponseRedirect(reverse('stream_view', args=[id, session_id]))
