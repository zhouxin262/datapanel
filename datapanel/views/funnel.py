#coding=utf-8
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import redirect_to_login

from datapanel.forms import FunnelForm, FunnelTesterForm
from datapanel.models import Funnel, FunnelAction

def home(request,id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel_list = Funnel.objects.filter(project=project)
    if not funnel_list:
        return HttpResponseRedirect(reverse('funnel_create', args=[id]))
    return render(request, 'datapanel/funnel/home.html',{'project':project,'funnel_list':funnel_list,})

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
            return HttpResponseRedirect(reverse('funnel_list', args=[id]))
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
    return render(request, 'datapanel/funnel/update.html', {'project':project, 'form': form})


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

def testercreate(request, id, funnel_id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = Funnel.objects.get(project=project, id = funnel_id)
    form = FunnelTesterForm()
    if request.method=="POST":
        form = FunnelTesterForm(request.POST)
        if form.is_valid():
            tester = form.save(commit=False)
            tester.funnel = funnel
            tester.save()
            return HttpResponseRedirect(reverse('funnel_testerlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/create.html', {'project':project, 'form': form})

def testerupdate(request, id, funnel_id, tester_id):
    try:
        project = request.user.participate_projects.get(id = id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    t = get_object_or_404(FunnelTester, pk=tester_id)
    form = FunnelTesterForm(instance=t)
    if request.method == 'POST':
        form = FunnelTesterForm(request.POST,instance=t)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('funnel_testerlist', args=[id, funnel_id]))
    return render(request, 'datapanel/funnel/update.html', {'project':project, 'form': form})


def testerdelete(request,id,funnel_id, tester_id):
    t = get_object_or_404(FunnelTester, pk=tester_id)
    t.delete()
    return HttpResponseRedirect(reverse('funnel_testerlist', args=[id, funnel_id]))

def testerlist(request,id, funnel_id):
    project = request.user.participate_projects.get(id = id)
    funnel = Funnel.objects.get(project=project, id = funnel_id)
    tester_list = funnel.tracktester.all()
    return render(request, 'datapanel/funnel/tester/list.html',{'project':project, 'funnel': funnel, 'tester_list':tester_list,})
