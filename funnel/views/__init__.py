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
from funnel.models import Funnel
from track.models import Track
from project.models import Action


def home(request, id):
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())
    params = {}

    start_date = request.GET.get('s', (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d"))
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
            #args = {'dateline__gte': start_date, 'dateline__lte': end_date}
            args = {}
            args['project'] = project
            args['from_action'] = from_action.action
            args['to_action'] = funnel_action.action
            data.append([funnel_action.action.name, Track.objects.filter(**args).aggregate(Count('session'))['session__count']])
        else:
            #args = {'dateline__gte': start_date, 'dateline__lte': end_date}
            args = {}
            args['session__project'] = project
            args['action'] = funnel_action.action
            data.append([funnel_action.action.name, Track.objects.filter(**args).aggregate(Count('session'))['session__count']])

        from_action = funnel_action
    data = simplejson.dumps(data)
    return render(request, 'datapanel/funnel/home.html', {'project': project, 'data': data, 'funnel_list': funnel_list, 'params': params})


def get_regular_funnel(project, max_action):
    funnel = [max_action, ]
    actions = [action for action in Action.objects.filter(project = project)]
    funnel_tuple = []
    # funnel_tree = {}

    s = datetime.now() - timedelta(days = 1)
    e = datetime.now()

    args = {}
    args['session__project'] = project
    args['action'] = max_action
    args['dateline__gte'] = s
    args['dateline__lte'] = e
    max_count = Track.objects.filter(**args).values('session').distinct().count()
    # print max_action, max_count
    funnel_tuple.append((max_action, max_count))

    # step = 1
    # funnel_tree[step] = [(max_action, max_count), ]
    # from_action = Action.objects.get(id = 4)
    while max_count:
        max_action = None
        max_count = 0
        if funnel[-1]:
            args = {}
            args['session__project'] = project
            args['dateline__gte'] = s
            args['dateline__lte'] = e
            for j, from_action in enumerate(funnel[::-1]):
                args["__".join(["from_track" for k in range(j+1)]) + "__action_id"] = from_action.id
            # print args
            ts = Track.objects.filter(**args).exclude(action__in = funnel).values('action').annotate(c = Count('id')).order_by('-c')
            # print ts
            if ts and ts[0]['c']  > 0:
                max_action = Action.objects.get(pk = ts[0]['action'])
                max_count = Track.objects.filter(**args).values('session').distinct().count()
                funnel.append(max_action)
                funnel_tuple.append((max_action, max_count))
        #     actions.remove(funnel[-1])

        #     for action in actions:
        #         args['action'] = action
        #         count = Track.objects.filter(**args).values('session').distinct().count()
        #         if count > max_count:
        #             max_count = count
        #             max_action = action

        # if max_action and max_count != 0:


    #     step += 1
    #     funnel_tree[step] = []

    #     if count > 0:
    #         insert_point = 0
    #         for a_c in funnel_tree[step]:
    #             if count <= a_c[1]:
    #                 insert_point += 1
    #             else:
    #                 break
    #         funnel_tree[step].insert(insert_point, (action, count))
    # print funnel_tree
    return funnel_tuple

def intel(request, id):
    print datetime.now()
    try:
        project = request.user.participate_projects.get(id=id)
    except AttributeError:
        return redirect_to_login(request.get_full_path())

    funnel = []
    if request.GET.get('action_id'):
        action = get_object_or_404(Action, id=request.GET.get('action_id'))
        funnel = get_regular_funnel(project, action)

    actions = Action.objects.filter()
    print datetime.now()
    return render(request, 'datapanel/funnel/intel.html', {'project': project, 'actions': actions, 'funnel': funnel})

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
