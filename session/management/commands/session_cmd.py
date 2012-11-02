#coding=utf-8
import os, sys
from django.db.models import Max
import datetime
from django.core.management.base import NoArgsCommand
from project.models import Project
from session.models import SessionGroupByTime, Session


class Command(NoArgsCommand):

    def handle(self, *args, **options):
        sgbt_max = SessionGroupByTime.objects.all().aggregate(Max('id'))
        projects = Project.objects.all()
        for project in projects:
            sessions = Session.objects.filter(project = project).order_by('start_time')
            i = 0
            j = 0
            start_time = sessions[0].start_time
            hourline = start_time.strftime('%Y%m%d%H')
            dayline = start_time.strftime('%Y%m%d')
            for s in sessions[1:]:
                s_hourline = s.start_time.strftime('%Y%m%d%H')
                s_dayline = s.start_time.strftime('%Y%m%d')
                if s_hourline == hourline:
                    i += 1
                else:
                    sessionGroupByTime = SessionGroupByTime()
                    sessionGroupByTime.project = project
                    sessionGroupByTime.datetype = "hourline"
                    sessionGroupByTime.dateline = start_time.replace(minute=0, second=0, microsecond=0)
                    sessionGroupByTime.value = i
                    sessionGroupByTime.save()
                    j = j +i
                    i= 0
                    hourline = s_hourline
                    start_time = s.start_time
                if s_dayline != dayline:
                    sessionGroupByTime = SessionGroupByTime()
                    sessionGroupByTime.project = project
                    sessionGroupByTime.datetype = "dayline"
                    sessionGroupByTime.dateline = start_time-datetime.timedelta(days=1)
                    sessionGroupByTime.value = j
                    sessionGroupByTime.save()
                    j = 0
                    dayline = s_dayline
                    start_time = s.start_time


