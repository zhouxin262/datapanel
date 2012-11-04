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
from funnel.models import Funnel, Swipe
from track.models import Track


def home(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    params = {}

    start_date = request.GET.get('s', (datetime.today() - timedelta(day=1)).strftime("%Y-%m-%d"))
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
            args = {'dateline__gte': start_date, 'dateline__lte': end_date}
            args['project'] = project
            args['from_action'] = from_action.action
            args['to_action'] = funnel_action.action
            data.append([funnel_action.action.name, Swipe.objects.filter(**args).aggregate(Count('session'))['session__count']])
        else:
            args = {'dateline__gte': start_date, 'dateline__lte': end_date}
            args['session__project'] = project
            args['action'] = funnel_action.action
            data.append([funnel_action.action.name, Track.objects.filter(**args).aggregate(Count('session'))['session__count']])

        from_action = funnel_action
    data = simplejson.dumps(data)
    return render(request, 'datapanel/funnel/home.html', {'project': project, 'data': data, 'funnel_list': funnel_list, 'params': params})


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
