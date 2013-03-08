 # coding=utf-8
import time
import json
from datetime import datetime, timedelta

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page

from project.forms import ProjectForm
from session.models import Session, GTime
from track.models import Track
from datapanel.models import Timeline


def create(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            import md5
            # project.token = md5.new(str(project.id + time.mktime(project.dateline.timetuple()))).hexdigest()
            project.token = md5.new(str(project.id + 54321)).hexdigest()
            project.participants.add(request.user)
            project.save()
            return HttpResponseRedirect(reverse('project_home', args=[project.id]))
    return render(request, 'project/create.html', {'form': form})


def overview(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    return render(request, 'project/overview.html', {'project': project, })


# @cache_page(60 * 60 * 24)
def home(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    # save for update the last view datetime
    project.save()

    d = request.GET.get('d', 'hour')
    s = request.GET.get('s', datetime.today().strftime("%Y-%m-%d"))
    e = request.GET.get('e', (datetime.strptime(s, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"))

    report = []

    ts = Timeline.objects.filter(datetype=d, dateline__range=[s, e])
    for t in ts:
        if t.dateline < datetime.now():
            try:
                gt = GTime.objects.get(project=project, timeline=t)
            except:
                gt = GTime.objects.generate(project, t, True)
        report.append([time.mktime(t.dateline.timetuple()) * 1000, gt.count])

    if request.is_ajax():
        return HttpResponse(json.dumps(report), mimetype="application/json")
    return render(request, 'project/index.html', {'project': project, 'report': json.dumps(report)})


def monitor(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    if request.is_ajax():
        e = datetime.now()
        s = e - timedelta(seconds=60)
        if request.GET.get('track'):
            y = Track.objects.filter(project=project, dateline__range=[s, e]).count()
            return HttpResponse(y)
        elif request.GET.get('session'):
            y = Session.objects.filter(project=project, start_time__range=[s, e]).count()
            return HttpResponse(y)
    return render(request, 'project/monitor.html', {'project': project, })


def setting(request, id):
    project = request.user.participate_projects.get(id=id)
    return render(request, 'project/setting.html', {'project': project})


def delete(request, id):
    project_name = request.POST.get('project_name', None)
    project = request.user.participate_projects.get(id=id, name=project_name)
    project.delete()
    return HttpResponseRedirect(reverse('index'))
