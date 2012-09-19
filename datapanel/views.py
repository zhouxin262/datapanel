#coding=utf-8
import datetime
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.db.models import Count,Avg

from datapanel.common import tongji
from datapanel.forms import ProjectForm
from datapanel.models import Project,Session,Track,TrackGroup

def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('auth_login'))
	if not request.user.participate_projects.all():
		return HttpResponseRedirect(reverse('datapanel_create'))
	else:
		lastview = request.user.participate_projects.order_by('-lastview')[0]
		return HttpResponseRedirect(reverse('datapanel_home', args=[lastview.id]))

def home(request, id):
	project = request.user.participate_projects.get(id = id)
	project.save() #更新lastview
	data = {}
	data['pv'] = Track.objects.filter(session__project = project).count()
	data['uv'] = Session.objects.filter(project = project).count()

	today = datetime.date.today()
	action_list = Track.objects.filter(session__project = project).values('action')
	track_list = {}
	for a in action_list:
		track_list[a['action']] = Track.objects.filter(session__project = project, action=a['action'])
	#dateline__range = [datetime.date(today.year, today.month, today.day), datetime.date(today.year, today.month, today.day)]

	return render(request, 'datapanel/index.html', {'project' : project, 'data': data, 'track_list': track_list})

def setting(request, id):
	project = request.user.participate_projects.get(id = id)
	return render(request, 'datapanel/setting.html', {'project':project})

def delete(request, id):
	project_name = request.POST.get('project_name', None)
	project = request.user.participate_projects.get(id = id, name=project_name)
	project.delete()
	return HttpResponseRedirect(reverse('datapanel_index'))

def create(request):
	form = ProjectForm()
	if request.method=="POST":
		form = ProjectForm(request.POST)
		if form.is_valid():
			project = form.save(commit=False)
			project.creator = request.user
			project.save()
			import time, md5
			#project.token = md5.new(str(project.id + time.mktime(project.dateline.timetuple()))).hexdigest()
			project.token = md5.new(str(project.id + 54321)).hexdigest()
			project.participants.add(request.user)
			project.save()
			return HttpResponseRedirect(reverse('datapanel_home', args=[project.id]))
			
	return render(request, 'datapanel/create.html', {'form': form})

def stream(request, id):
	project = request.user.participate_projects.get(id = id)
	return render(request, 'datapanel/stream.html', {'project':project})

def stream_detail(request, id, sid):
	project = request.user.participate_projects.get(id = id)
	session = project.session.get(id=sid)
	track_flow = session.track.all().order_by('dateline')
	return render(request, 'datapanel/stream_detail.html', {'project':project,'track_flow':track_flow})


def dealdate(groupdate,stime,interval):
	if groupdate == 'H':
		stime = stime- datetime.timedelta(hours=int(interval))
		d3time = stime- datetime.timedelta(hours=int(interval))
		d = str(d3time.month) +'月'+str(d3time.day)+'日' + str(d3time.hour)+'时'
	elif groupdate == 'D':
		stime = stime- datetime.timedelta(days=int(interval))
		d3time = stime- datetime.timedelta(days=int(interval))
		d = str(d3time.month) +'月'+str(d3time.day)+'日' 
	elif groupdate == 'W':
		stime = stime - datetime.timedelta(days=(int(interval)*7))
		d3time = stime - datetime.timedelta(days=7)
		d = str(d3time.month) +'月'+str(d3time.day)+'日' 
	elif groupdate == 'M':
		if stime.month >int(interval):
			stime = stime.replace(month = stime.month - int(interval),day=1,hour=0, minute=0, second=0, microsecond=0)
		else:
			stime = stime.replace(year = (stime.year - int((int(interval)-stime.month)/12)),month = (12-(int(interval)-stime.month)%12),day=1,hour=0, minute=0, second=0, microsecond=0)
		
		if stime.month >1:
			d3time = stime.replace(month = stime.month - 1,day=1,hour=0, minute=0, second=0, microsecond=0)
		else:
			d3time = stime.replace(year = (stime.year - 1),month = 12,day=1,hour=0, minute=0, second=0, microsecond=0)
		d = str(d3time.year)+'年' + str(d3time.month) +'月'
	else:
		d = ''
	return {'d':d,'stime':stime}
	
def group(request, id):
	project = request.user.participate_projects.get(id = id)
	grouptype = request.GET.get('grouptype','A')
	datatype = request.GET.get('datatype','C')
	groupcate = request.GET.get('groupcate','A')
	groupdate = request.GET.get('groupdate','D')
	interval = request.GET.get('interval','1')
	timeline = request.GET.get('timeline','0')
	params = {'grouptype':grouptype,'datatype':datatype,'groupcate':groupcate,'groupdate':groupdate,'interval':interval,'timeline':timeline}
	data = {}
	delta = datetime.datetime.now()
	stime = ''
	d1 = ''
	d2 = ''
	if grouptype == 'A':
		alias = 'action'
	elif grouptype == 'U':
		alias = 'url'
	else:
		alias = 'action'
	if int(timeline) == 0:
		params['ptimeline'] = '0'
		params['ntimeline'] = '1'
		etime = delta
		if groupdate == 'H':
			stime = delta.replace(minute=0, second=0, microsecond=0)
			d1 = str(delta.month) +'月'+str(delta.day)+'日' + str(delta.hour)+'时'
			d2time = stime- datetime.timedelta(hours=int(interval))
			d2 = str(d2time.month) +'月'+str(d2time.day)+'日' + str(d2time.hour)+'时'
		elif groupdate == 'D':
			stime = delta.replace(hour=0, minute=0, second=0, microsecond=0)
			d1 = str(delta.month) +'月'+str(delta.day)+'日' 
			d2time = stime- datetime.timedelta(days=int(interval))
			d2 = str(d2time.month) +'月'+str(d2time.day)+'日' 
		elif groupdate == 'W':
			stime = delta.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=etime.weekday())
			d1 = str(stime.month) +'月'+str(stime.day)+'日' 
			d2time = delta.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=delta.weekday()) - datetime.timedelta(int(interval)*7)
			d2 = str(d2time.month) +'月'+str(d2time.day)+'日' 
		elif groupdate == 'M':
			stime = delta.replace(day=1,hour=0, minute=0, second=0, microsecond=0)
			d1 = str(stime.year)+'年' + str(stime.month) +'月'
			if stime.month >int(interval):
				d2time = stime.replace(month = stime.month - int(interval),day=1,hour=0, minute=0, second=0, microsecond=0)
			else:
				d2time = stime.replace(year = (stime.year - int((int(interval)-stime.month)/12)),month = (12-(int(interval)-stime.month)%12),day=1,hour=0, minute=0, second=0, microsecond=0)
			d2 = str(d2time.year)+'年' + str(d2time.month) +'月'
			
		c = tongji(starttime=stime, endtime=etime, grouptype =grouptype, datatype = datatype, groupcate = groupcate, groupdate=groupdate, save = False)
		
		for a in c:
			data[a[alias]] = {d1:a['val']}	
		tg2 = TrackGroup.objects.filter(dateline = stime,grouptype = grouptype,groupcate=groupcate,groupdate =groupdate,datatype=datatype)
		if tg2:
			for t in tg2:
				if data.has_key(t.name):
					data2 = data[t.name]
					data2[d2] = t.count
					data[t.name] = data2
				else:
					data[t.name] = {d1:0,d2:t.count}
	else:
		params['ptimeline'] = str(int(timeline) -1)
		params['ntimeline'] = str(int(timeline) +1)
		if groupdate == 'H':
			stime = delta.replace(minute=0, second=0, microsecond=0)- datetime.timedelta(hours=(int(timeline)*int(interval)*5 -1))
			d1time = stime- datetime.timedelta(hours=1)
			d1 = str(d1time.month) +'月'+str(d1time.day)+'日' + str(d1time.hour)+'时'
		elif groupdate == 'D':
			stime = delta.replace(hour=0, minute=0, second=0, microsecond=0)- datetime.timedelta(days=(int(timeline)*int(interval)*5)-1)
			d1time = stime- datetime.timedelta(days=1)
			d1 = str(d1time.month) +'月'+str(d1time.day)+'日' 
		elif groupdate == 'W':
			stime = delta.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=delta.weekday()) - datetime.timedelta(days=((int(timeline)*int(interval)*5)-1)*7)
			d1time = delta.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=delta.weekday())
			d1 = str(stime.month) +'月'+str(stime.day)+'日' 
		elif groupdate == 'M':
			if delta.month >(int(timeline)*int(interval)*5 -1):
				stime = delta.replace(month = delta.month - (int(timeline)*int(interval)*5 -1),day=1,hour=0, minute=0, second=0, microsecond=0)
			else:
				stime = delta.replace(year = (delta.year - int(((int(timeline)*int(interval)*5 -1)-delta.month)/12)),month = (12-((int(timeline)*int(interval)*5 -1)-delta.month)%12),day=1,hour=0, minute=0, second=0, microsecond=0)
				
			if stime.month >1:
				d1time = stime.replace(month = stime.month -1,day=1,hour=0, minute=0, second=0, microsecond=0)
			else:
				d1time = stime.replace(year = (stime.year - 1),month = 12,day=1,hour=0, minute=0, second=0, microsecond=0)
			d1 = str(d1time.year)+'年' + str(d1time.month) +'月'
		tg1 = TrackGroup.objects.filter(dateline = stime,grouptype = grouptype,groupcate=groupcate,groupdate =groupdate,datatype=datatype)
		if tg1:
			for t in tg1:
				data[t.name] = {d1:t.count}	
				
		dd2 = dealdate(groupdate,stime,interval)
		stime = dd2['stime']
		d2 = dd2['d']
		tg2 = TrackGroup.objects.filter(dateline = stime,grouptype = grouptype,groupcate=groupcate,groupdate =groupdate,datatype=datatype)
		if tg2:
			for t in tg2:
				if data.has_key(t.name):
					data2 = data[t.name]
					data2[d2] = t.count
					data[t.name] = data2
				else:
					data[t.name] = {d1:0,d2:t.count}

	dd3 = dealdate(groupdate,stime,interval)
	stime = dd3['stime']
	d3 = dd3['d']
	tg3 = TrackGroup.objects.filter(dateline = stime,grouptype = grouptype,groupcate=groupcate,groupdate =groupdate,datatype=datatype)
	if tg3:
		for t in tg3:
			if data.has_key(t.name):
				data3 = data[t.name]
				data3[d3] = t.count
				data[t.name] = data3
			else:
				data[t.name] = {d1:0,d2:0,d3:t.count}
				
	dd4 = dealdate(groupdate,stime,interval)
	stime = dd4['stime']
	d4 = dd4['d']
	tg4 = TrackGroup.objects.filter(dateline = stime,grouptype = grouptype,groupcate=groupcate,groupdate =groupdate,datatype=datatype)
	if tg4:
		for t in tg4:
			if data.has_key(t.name):
				data4 = data[t.name]
				data4[d4] = t.count
				data[t.name] = data4
			else:
				data[t.name] = {d1:0,d2:0,d3:0,d4:t.count}

	dd5 = dealdate(groupdate,stime,interval)
	stime = dd5['stime']
	d5 = dd5['d']
	tg5 = TrackGroup.objects.filter(dateline = stime,grouptype = grouptype,groupcate=groupcate,groupdate =groupdate,datatype=datatype)
	if tg5:
		for t in tg5:
			if data.has_key(t.name):
				data5 = data[t.name]
				data5[d5] = t.count
				data[t.name] = data5
			else:
				data[t.name] = {d1:0,d2:0,d3:0,d4:0,d5:t.count}
				
	return render(request, 'datapanel/group.html', {'project':project,'data':data,'d1':d1,'d2':d2,'d3':d3,'d4':d4,'d5':d5,'params':params})

def track(request):
	token = request.GET.get('k', None)
	if token:
		p = Project.objects.get(token = token)
		s = Session.objects.get_or_create(sn =request.session.session_key,
			project=p,
			user_timezone = request.META.get('TZ',''),
			user_agent = request.META.get('HTTP_USER_AGENT',''),
			ipaddress = request.META.get('REMOTE_ADDR',''))
		if s[1]:
			s[0].save()
		s = s[0]
		t = Track()
		t.session = s
		t.action = request.GET.get('t','')
		t.url = request.META.get('HTTP_REFERER','')
		t.param = request.GET.get('p','')
		t.step = 0
		t.mark = 0
		t.timelength = 0
		t.save()
	response_data = {}
	response_data['result'] = 'success'
	response_data['message'] = ''
	return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")