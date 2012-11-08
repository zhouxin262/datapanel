#coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import redirect_to_login

from project.models import Action
from funnel.forms import FunnelActionForm
from funnel.models import Funnel, FunnelAction


def create(request, id, funnel_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = Funnel.objects.get(project=project, id=funnel_id)
    form = FunnelActionForm()
    form.fields['action'].queryset = Action.objects.filter(project=project)
    if request.method == "POST":
        form = FunnelActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.funnel = funnel
            action.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project': project,'funnel':funnel, 'form': form})


def update(request, id, funnel_id, action_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    t = get_object_or_404(FunnelAction, pk=action_id)
    form = FunnelActionForm(instance=t)
    form.fields['action'].queryset = Action.objects.filter(project=project)
    if request.method == 'POST':
        form = FunnelActionForm(request.POST, instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project': project, 'form': form})


def delete(request, id, funnel_id, action_id):
    t = get_object_or_404(FunnelAction, pk=action_id)
    t.delete()
    return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))


def list(request, id, funnel_id):
    project = request.user.participate_projects.get(id=id)
    funnel = Funnel.objects.get(project=project, id=funnel_id)
    action_list = funnel.action.filter().order_by('order')
    return render(request, 'datapanel/funnel/action/list.html', {'project': project, 'funnel': funnel, 'action_list': action_list, })

def up(request, id, funnel_id, action_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    t = get_object_or_404(FunnelAction, pk=action_id)
    form = FunnelActionForm(instance=t)
    form.fields['action'].queryset = Action.objects.filter(project=project)
    if request.method == 'POST':
        form = FunnelActionForm(request.POST, instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project': project, 'form': form})

def down(request, id, funnel_id, action_id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    t = get_object_or_404(FunnelAction, pk=action_id)
    form = FunnelActionForm(instance=t)
    form.fields['action'].queryset = Action.objects.filter(project=project)
    if request.method == 'POST':
        form = FunnelActionForm(request.POST, instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('funnel_actionlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project': project, 'form': form})
