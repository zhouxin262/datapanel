#coding=utf-8
def home(request, id):
    project = request.user.participate_projects.get(id = id)
    grouptype = request.GET.get('grouptype','A')
    datatype = request.GET.get('datatype','C')
    groupcate = request.GET.get('groupcate','A')
    groupdate = request.GET.get('groupdate','D')
    interval = int(request.GET.get('interval',1))
    timeline = int(request.GET.get('timeline',0))
    params = {'grouptype':grouptype,'datatype':datatype,'groupcate':groupcate,'groupdate':groupdate,'interval':interval,'timeline':timeline}

    # 处理时间
    times = []
    if groupdate == 'H':
        for i in range(5):
            times.append(datetime.datetime.now(UTC()).replace(minute=0, second=0, microsecond=0) - datetime.timedelta(hours=i*interval + timeline))
    elif groupdate == 'D':
        for i in range(5):
            times.append(datetime.datetime.now(UTC()).replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=i*interval + timeline))
    elif groupdate == 'W':
        for i in range(5):
            times.append(datetime.datetime.now(UTC()).replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=datetime.datetime.now(UTC()).weekday()) - datetime.timedelta(days=7*i*interval + timeline*7))
    elif groupdate == 'M':
        for i in range(5):
            month = ( datetime.datetime.now(UTC()).month + i*interval + timeline ) % 12
            if month == 0:
                month = 12
            times.append(datetime.datetime.now(UTC()).replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0))

    trackgroup_list = TrackGroup.objects.filter(project = project, grouptype = grouptype, datatype = datatype, groupcate = groupcate, groupdate = groupdate, dateline__in = times).order_by('name','-dateline')
    return render(request, 'datapanel/group/home.html', {'project':project,'params':params, 'trackgroup_list': trackgroup_list, 'times': times})