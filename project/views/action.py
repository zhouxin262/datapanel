#coding=utf-8
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from project.forms import ActionForm
from project.models import Action


def create(request, id):
    project = request.user.participate_projects.get(id=id)
    form = ActionForm()
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.project = project
            action.save()
            return HttpResponseRedirect(reverse('action_list', args=[id]))
    return render(request, 'project/action/create.html', {'project': project, 'form': form})


def update(request, id, aid):
    project = request.user.participate_projects.get(id=id)
    action = get_object_or_404(Action, pk=aid)
    form = ActionForm(instance=action)
    if request.method == 'POST':
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            action = form.save()
            return HttpResponseRedirect(reverse('action_list', args=[action.project.id]))
    return render(request, 'project/action/update.html', {'project': project, 'form': form})


def delete(request, id, aid):
    action = get_object_or_404(Action, project_id=id, id=aid)
    action.delete()
    return HttpResponseRedirect(reverse('action_list', args=[id]))


def list(request, id):
    project = request.user.participate_projects.get(id=id)
    project_actions = Action.objects.filter(project_id=id)
    paginator = Paginator(project_actions, 25)
    page = request.GET.get('page')
    try:
        action_list = paginator.page(page)
    except PageNotAnInteger:
        action_list = paginator.page(1)
    except EmptyPage:
        action_list = paginator.page(paginator.num_pages)
    page_range = range(100)
    return render(request, 'project/action/list.html', {'project': project, 'action_list': action_list, 'page_range': page_range})
