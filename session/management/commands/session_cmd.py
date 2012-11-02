#coding=utf-8
import os, sys
from django.db.models import Max
import datetime
from django.core.management.base import NoArgsCommand
from datapanel.models import CmdSerialNumber
from project.models import Project
from session.models import SessionGroupByTime, Session


class Command(NoArgsCommand):

    def handle(self, *args, **options):
        cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'sessiongroupbytime', class_name='Session')
        last_id = cmdSerialNumber[0].last_id
        projects = Project.objects.all()
        for project in projects:
            sessions = Session.objects.filter(project = project,id__gt = last_id).order_by('start_time')
            start_time = sessions[0].start_time
            hour_value = 0
            day_value = 0
            week_value = 0
            month_value = 0
            hour = sessions[0].get_time("hour")
            day = sessions[0].get_time("day")
            week = sessions[0].get_time("week")
            month = sessions[0].get_time("month")
            for s in sessions:
                s_hour = s.get_time("hour")
                s_day = s.get_time("day")
                s_week = s.get_time("week")
                s_month = s.get_time("month")
                if s_hour == hour:
                    hour_value += 1
                else:
                    SessionGroupByTime.objects.get_or_create(project=project,datetype="hour",dateline=hour,value = hour_value)
                    day_value += hour_value
                    hour_value= 0
                    hour = s_hour
                if s_day != day:
                    SessionGroupByTime.objects.get_or_create(project=project,datetype="day",dateline=day,value = day_value)
                    week_value += day_value
                    day_value = 0
                    day = s_day
                if s_week != week:
                    SessionGroupByTime.objects.get_or_create(project=project,datetype="week",dateline=week,value = week_value)
                    month_value += day_value
                    week_value = 0
                    week = s_week
                if s_month != month:
                    SessionGroupByTime.objects.get_or_create(project=project,datetype="month",dateline=month,value = month_value)
                    month_value = 0
                    month = s_month

                cmdSerialNumber[0].last_id = s.id
                cmdSerialNumber[0].save()


