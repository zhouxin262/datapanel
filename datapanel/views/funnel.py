#coding=utf-8
from datetime import datetime
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.utils import simplejson

from datapanel.forms import FunnelForm, FunnelActionForm
from datapanel.models import Funnel, FunnelAction, Action, Session

def home(request,id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    params = {}

    start_date = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
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

    args = {'track_count__gt': 1, 'end_time__gte': start_date, 'start_time__lte': end_date}
    print args

    y = [a.action.name for a in f.action.filter().order_by('order')]
    funnel_actions = [";".join(y[:i+1]) for i in range(len(y))]
    data = []
    for funnel_action in funnel_actions:
        args['stream_str__contains'] = funnel_action
        data.append([y[funnel_actions.index(funnel_action)], Session.objects.filter(**args).count()])
    data = simplejson.dumps(data)
    return render(request, 'datapanel/funnel/home.html',{'project':project,'data':data, 'funnel_list':funnel_list, 'params':params})

def create(request,id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    form = FunnelForm()
    if request.method=="POST":
        form = FunnelForm(request.POST)
        if form.is_valid():
            funnel = form.save(commit=False)
            funnel.project = project
            funnel.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel.id]))
    return render(request, 'datapanel/funnel/create.html', {'project':project, 'form': form})

def update(request,id,funnel_id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = get_object_or_404(Funnel, pk=funnel_id)
    form = FunnelForm(instance=funnel)
    if request.method == 'POST':
        form = FunnelForm(request.POST,instance=funnel)
        if form.is_valid():
            funnel = form.save()
            return HttpResponseRedirect(reverse('funnel_list', args=[id]))
    return render(request, 'datapanel/funnel/create.html', {'project':project, 'form': form})


def delete(request,id,funnel_id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = get_object_or_404(Funnel, pk=funnel_id)
    funnel.delete()
    return HttpResponseRedirect(reverse('funnel_list', args=[id]))

def list(request,id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel_list = Funnel.objects.filter(project=project)
    return render(request, 'datapanel/funnel/list.html',{'project':project,'funnel_list':funnel_list,})

def actioncreate(request, id, funnel_id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = Funnel.objects.get(project=project, id = funnel_id)
    form = FunnelActionForm()
    form.fields['action'].queryset = Action.objects.filter(project=project)
    if request.method=="POST":
        form = FunnelActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.funnel = funnel
            action.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project':project, 'form': form})

def actionupdate(request, id, funnel_id, action_id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    t = get_object_or_404(FunnelAction, pk=action_id)
    form = FunnelActionForm(instance=t)
    form.fields['action'].queryset = Action.objects.filter(project=project)
    if request.method == 'POST':
        form = FunnelActionForm(request.POST,instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project':project, 'form': form})


def actiondelete(request,id,funnel_id, action_id):
    t = get_object_or_404(FunnelAction, pk=action_id)
    t.delete()
    return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))

def actionlist(request,id, funnel_id):
    project = request.user.participate_projects.get(id = id)
    funnel = Funnel.objects.get(project=project, id = funnel_id)
    action_list = funnel.action.filter().order_by('order')
    return render(request, 'datapanel/funnel/action/list.html',{'project':project, 'funnel': funnel, 'action_list':action_list,})
