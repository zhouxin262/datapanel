#coding=utf-8
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from datapanel.forms import ConditionForm, ConditionTesterForm
from datapanel.models import TrackCondition, TrackConditionTester

def create(request,id):
    project = request.user.participate_projects.get(id = id)
    form = ConditionForm()
    if request.method=="POST":
        form = ConditionForm(request.POST)
        if form.is_valid():
            condition = form.save(commit=False)
            condition.project = project
            condition.save()
            return HttpResponseRedirect(reverse('condition_list', args=[id]))
    return render(request, 'datapanel/condition/create.html', {'project':project, 'form': form})

def update(request,id,condition_id):
    project = request.user.participate_projects.get(id = id)
    condition = get_object_or_404(TrackCondition, pk=condition_id)
    form = ConditionForm(instance=condition)
    if request.method == 'POST':
        form = ConditionForm(request.POST,instance=condition)
        if form.is_valid():
            condition = form.save()
            return HttpResponseRedirect(reverse('condition_list', args=[id]))
    return render(request, 'datapanel/condition/update.html', {'project':project, 'form': form})


def delete(request,id,condition_id):
    condition = get_object_or_404(TrackCondition, pk=condition_id)
    condition.delete()
    return HttpResponseRedirect(reverse('condition_list', args=[id]))

def list(request,id):
    project = request.user.participate_projects.get(id = id)
    condition_list = TrackCondition.objects.filter(project=project)
    return render(request, 'datapanel/condition/list.html',{'project':project,'condition_list':condition_list,})

def testercreate(request, id, condition_id):
    project = request.user.participate_projects.get(id = id)
    condition = TrackCondition.objects.get(project=project, id = condition_id)
    form = ConditionTesterForm()
    if request.method=="POST":
        form = ConditionTesterForm(request.POST)
        if form.is_valid():
            tester = form.save(commit=False)
            tester.condition = condition
            tester.save()
            return HttpResponseRedirect(reverse('condition_testerlist', args=[id, condition_id]))
    return render(request, 'datapanel/condition/create.html', {'project':project, 'form': form})

def testerupdate(request, id, condition_id, tester_id):
    project = request.user.participate_projects.get(id = id)
    t = get_object_or_404(TrackConditionTester, pk=tester_id)
    form = ConditionTesterForm(instance=t)
    if request.method == 'POST':
        form = ConditionTesterForm(request.POST,instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('condition_testerlist', args=[id, condition_id]))
    return render(request, 'datapanel/condition/update.html', {'project':project, 'form': form})


def testerdelete(request,id,condition_id, tester_id):
    t = get_object_or_404(TrackConditionTester, pk=tester_id)
    t.delete()
    return HttpResponseRedirect(reverse('condition_testerlist', args=[id, condition_id]))

def testerlist(request,id, condition_id):
    project = request.user.participate_projects.get(id = id)
    condition = TrackCondition.objects.get(project=project, id = condition_id)
    tester_list = condition.tracktester.all()
    return render(request, 'datapanel/condition/tester/list.html',{'project':project, 'condition': condition, 'tester_list':tester_list,})
