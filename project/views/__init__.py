#coding=utf-8
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from project.forms import ProjectForm
from session.models import Session, SessionGroupByTime


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
    datetype = request.GET.get('datetype', 'hour')
    sbt = SessionGroupByTime.objects.filter(project=project, datetype=datetype)
    return render(request, 'project/index.html', {'project': project, 'sbt': sbt})


def setting(request, id):
    project = request.user.participate_projects.get(id=id)
    return render(request, 'project/setting.html', {'project': project})


def delete(request, id):
    project_name = request.POST.get('project_name', None)
    project = request.user.participate_projects.get(id=id, name=project_name)
    project.delete()
    return HttpResponseRedirect(reverse('index'))
