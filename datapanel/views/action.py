#coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datapanel.forms import ActionForm
from datapanel.models import Action

def create(request,id):
    form = ActionForm()
    if request.method=="POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save()
            return HttpResponseRedirect(reverse('action_view', args=[action.id]))
    return render(request, 'datapanel/action/create.html', {'form': form})


def update(request,id,aid):
    action = get_object_or_404(Action, pk=aid)
    form = ActionForm(instance=action)
    if request.method == 'POST':
        form = ActionForm(request.POST,instance=action)
        if form.is_valid():
            action = form.save()
            return HttpResponseRedirect(reverse('action_view', args=[action.id]))
    return render(request, 'datapanel/action/update.html',{'form': form})


def delete(request,id,aid):
    action = Action.objects.get(id=aid)
    action.delete()
    return HttpResponseRedirect(reverse('action_create'))


def view(request,id,aid):
    action = Action.objects.get(id=aid)
    return render(request, 'datapanel/action/view.html',{'action':action})

def list(request,id):
    project = request.user.participate_projects.get(id = id)
    action_list = Action.objects.filter(project_id=id)
    return render(request, 'datapanel/action/list.html',{'project':project,'action_list':action_list})
