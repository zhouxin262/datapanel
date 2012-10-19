#coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from datapanel.models import Referer

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
    project_sessions = project.session.all().order_by('-id')
    paginator = Paginator(project_sessions, 25)
    page = request.GET.get('page')
    try:
        session_list = paginator.page(page)
    except PageNotAnInteger:
        session_list = paginator.page(1)
    except EmptyPage:
        session_list = paginator.page(paginator.num_pages)
    return render(request, 'datapanel/stream/list.html', {'project':project,
        'session_list': session_list})

def view(request, id, sid):
    project = request.user.participate_projects.get(id = id)
    session = project.session.get(id=sid)
    track_flow = session.track.all().order_by('-dateline')
    return render(request, 'datapanel/stream/view.html', {'project':project,'track_flow':track_flow})

def referer_list(request, id):
    groupby = request.GET.get('groupby', 'keyword')
    keyword = request.GET.get('keyword', '')
    querystr = 'groupby=%s&keyword=%s' % (groupby, keyword)
    params = {'groupby':groupby , 'keyword':keyword, 'querystr':querystr}
    # deal with params
    project = request.user.participate_projects.get(id = id)
    args = {'session__project': project, groupby +'__contains': keyword}
    referers = Referer.objects.filter(**args).values(groupby).annotate(c = Count('id')).order_by('-c')
    paginator = Paginator(referers, 25)
    page = request.GET.get('page')
    try:
        referer_list = paginator.page(page)
    except PageNotAnInteger:
        referer_list = paginator.page(1)
    except EmptyPage:
        referer_list = paginator.page(paginator.num_pages)
    return render(request, 'datapanel/stream/referer_list.html', {'project':project, 'referer_list':referer_list,'params':params})