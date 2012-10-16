#coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

def list(request, id):
    project = request.user.participate_projects.get(id = id)

    # #排序
    # order = request.GET.get('order', 't')
    # if order == 'c':
    #     project_sessions = project.session.all().annotate(c=Count('track')).order_by('-c')
    # else:
    #     project_sessions = project.session.all().annotate(c=Count('track')).order_by('-end_time')

    #过滤
    # param_filter = request.GET.get('filter', '')
    # if param_filter:
    #     project_sessions = project_sessions.filter(param_contains = param_filter)
    project_sessions = project.session.all().order_by('-end_time')
    project_sessions = project_sessions[:1000]
    paginator = Paginator(project_sessions, 25)
    page = request.GET.get('page')
    try:
        session_list = paginator.page(page)
    except PageNotAnInteger:
        session_list = paginator.page(1)
    except EmptyPage:
        session_list = paginator.page(paginator.num_pages)
    page_range = range(100);
    return render(request, 'datapanel/stream/list.html', {'project':project,
        'session_list': session_list, 'page_range':page_range})

def view(request, id, sid):
    project = request.user.participate_projects.get(id = id)
    session = project.session.get(id=sid)
    track_flow = session.track.all().order_by('-dateline')
    return render(request, 'datapanel/stream/view.html', {'project':project,'track_flow':track_flow})