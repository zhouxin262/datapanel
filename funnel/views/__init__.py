#coding=utf-8
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.utils import simplejson
from django.db.models import Count

from funnel.forms import FunnelForm
from session.models import Session
from funnel.models import Funnel
from track.models import Track
from project.models import Action


def home(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    params = {}

    start_date = request.GET.get('s', (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"))
    end_date = request.GET.get('e', datetime.today().strftime("%Y-%m-%d"))

    funnel_list = Funnel.objects.filter(project=project)

    if not funnel_list:
        return HttpResponseRedirect(reverse('funnel_create', args=[id]))

    funnel_id = int(request.GET.get('funnel_id', 0))
    if funnel_id:
        f = Funnel.objects.get(project=project, id=funnel_id)
    else:
        f = Funnel.objects.filter(project=project)[0]
        funnel_id = f.id

    params['funnel'] = f.name

    # print args

    from_action = None
    data = []
    for funnel_action in f.action.filter().order_by('order'):
        if from_action:
            #args = {'dateline__gte': start_date, 'dateline__lte': end_date}
            args = {}
            args['project'] = project
            args['from_action'] = from_action.action
            args['to_action'] = funnel_action.action
            data.append([funnel_action.action.name, Swipe.objects.filter(**args).aggregate(Count('session'))['session__count']])
        else:
            #args = {'dateline__gte': start_date, 'dateline__lte': end_date}
            args = {}
            args['session__project'] = project
            args['action'] = funnel_action.action
            data.append([funnel_action.action.name, Track.objects.filter(**args).aggregate(Count('session'))['session__count']])

        from_action = funnel_action
    data = simplejson.dumps(data)
    return render(request, 'datapanel/funnel/home.html', {'project': project, 'data': data, 'funnel_list': funnel_list, 'params': params})


def get_regular_funnel(project, action = None):
    funnel = [action, ]
    count = 1
    # from_action = Action.objects.get(id = 4)
    while count:
        if funnel[-1]:
            args = {}
            # args['project'] = project
            for j, from_action in enumerate(funnel[::-1]):
                args["__".join(["from_track__swipe" for k in range(j+1)]) + "__action_id"] = from_action.id
            # print args
            swipe = Swipe.objects.filter(**args).exclude(action__in = funnel).values('action').annotate(c = Count('id')).order_by('-c')
        else:
            swipe = Swipe.objects.filter(project = project).values('action').annotate(c = Count('id')).order_by('-c')
        print args
        print Swipe.objects.filter(**args)
        if swipe and swipe[0]['c'] != 0:
            funnel.append(Action.objects.get(id = swipe[0]['action']))
            count = swipe[0]['c']
        else:
            count = 0
    return funnel

def intel(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    action = Action.objects.get(id = 4)
    print get_regular_funnel(project, action)
    return render(request, 'datapanel/funnel/intel.html')

def create(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    form = FunnelForm()
    if request.method == "POST":
        form = FunnelForm(request.POST)
        if form.is_valid():
            funnel = form.save(commit=False)
            funnel.project = project
            funnel.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel.id]))
    return render(request, 'datapanel/funnel/create.html', {'project': project, 'form': form})


def update(request, id, funnel_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = get_object_or_404(Funnel, pk=funnel_id)
    form = FunnelForm(instance=funnel)
    if request.method == 'POST':
        form = FunnelForm(request.POST, instance=funnel)
        if form.is_valid():
            funnel = form.save()
            return HttpResponseRedirect(reverse('funnel_list', args=[id]))
    return render(request, 'datapanel/funnel/create.html', {'project': project, 'form': form})


def delete(request, id, funnel_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = get_object_or_404(Funnel, pk=funnel_id, project=project)
    funnel.delete()
    return HttpResponseRedirect(reverse('funnel_list', args=[id]))


def list(request, id):

    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel_list = Funnel.objects.filter(project=project)
    return render(request, 'datapanel/funnel/list.html', {'project': project, 'funnel_list': funnel_list, })
