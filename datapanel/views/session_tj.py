#coding=utf-8
import os, sys
from django.db.models import Max
from datetime import datetime
from datapanel.models import Session, SessionGroupByTime, Project

def session_tj(request):
#    sgbt_max = SessionGroupByTime.objects.all().aggregate(Max('id'))
    projects = Project.objects.all()
    for project in projects:
        sessions = Session.objects.filter(project = project).order_by('start_time')
        i = 0
        start_time = sessions[0].start_time
        hourline = sessions[0].start_time.strftime('%Y%m%d%H')
        for s in sessions[1:]:
            start_time_format = s.start_time.strftime('%Y%m%d%H')
            if start_time_format == hourline:
                i += 1
            else:
                sessionGroupByTime = SessionGroupByTime()
                sessionGroupByTime.project = project
                sessionGroupByTime.datetype = "hourline"
                sessionGroupByTime.dateline = start_time.replace(minute=0, second=0, microsecond=0)
                sessionGroupByTime.value = i
                sessionGroupByTime.save()
                i= 0
                hourline = start_time_format
                start_time = s.start_time

