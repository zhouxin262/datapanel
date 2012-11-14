#coding=utf-8
from datetime import datetime, timedelta

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.db.models import Count
from datetime import datetime
from project.forms import ProjectForm
from session.models import Session, SessionGroupByTime
from track.models import Track


def create(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            import md5
            #project.token = md5.new(str(project.id + time.mktime(project.dateline.timetuple()))).hexdigest()
            project.token = md5.new(str(project.id + 54321)).hexdigest()
            project.participants.add(request.user)
            project.save()
            return HttpResponseRedirect(reverse('project_home', args=[project.id]))
    return render(request, 'project/create.html', {'form': form})


def home(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    project.save()
    interval = request.GET.get('interval', '0')
    datetype = ""
    if interval == "1":
        start_day = (datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d")
        end_day = (datetime.today()).strftime("%Y-%m-%d")
        datetype = "hour"
    elif interval == "7":
        start_day = (datetime.today()-timedelta(days=6)).strftime("%Y-%m-%d")
        end_day = (datetime.today()).strftime("%Y-%m-%d")
        datetype = "day"
    elif interval == "30":
        start_day = (datetime.today()-timedelta(days=30)).strftime("%Y-%m-%d")
        end_day = (datetime.today()).strftime("%Y-%m-%d")
    else:
        start_day = datetime.today().strftime("%Y-%m-%d")
        end_day = (datetime.today()+timedelta(days=1)).strftime("%Y-%m-%d")
        datetype = "hour"

    s1 = SessionGroupByTime.objects.filter(project=project, datetype=datetype,dateline__gte=start_day).order_by("dateline")
    s2 = s1.exclude(dateline__gte=end_day)
    return render(request, 'project/index.html', {'project': project, 'sbt': s2,'interval':interval})

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
