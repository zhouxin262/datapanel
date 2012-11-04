#coding=utf-8
import os
import sys
import datetime

from django.db.models import Max, Sum, Count
from django.core.management.base import LabelCommand

from datapanel.models import CmdSerialNumber
from project.models import Project
from session.models import SessionGroupByTime, Session
from track.models import TrackValue


class Command(LabelCommand):

    def handle_label(self, label, *args, **options):
        if label == 'groupby':
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'sessiongroupbytime', class_name='Session')
            last_id = cmdSerialNumber[0].last_id
            projects = Project.objects.all()
            for project in projects:
                sessions = Session.objects.filter(project = project,id__gt = last_id).order_by('start_time')
                if len(sessions)>0:
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
                            sgbt = SessionGroupByTime.objects.get_or_create(project=project,datetype="hour",dateline=hour)
                            sgbt[0].value += hour_value
                            sgbt[0].save()
                            day_value += hour_value
                            hour_value= 0
                            hour = s_hour
                        if s_day != day:
                            sgbt = SessionGroupByTime.objects.get_or_create(project=project,datetype="day",dateline=day)
                            sgbt[0].value += day_value
                            sgbt[0].save()
                            week_value += day_value
                            day_value = 0
                            day = s_day
                        if s_week != week:
                            sgbt = SessionGroupByTime.objects.get_or_create(project=project,datetype="week",dateline=week)
                            sgbt[0].value += week_value
                            sgbt[0].save()
                            month_value += day_value
                            week_value = 0
                            week = s_week
                        if s_month != month:
                            sgbt = SessionGroupByTime.objects.get_or_create(project=project,datetype="month",dateline=month)
                            sgbt[0].value += month_value
                            sgbt[0].save()
                            month_value = 0
                            month = s_month

                        cmdSerialNumber[0].last_id = s.id
                        cmdSerialNumber[0].save()

        elif label == 'referer':
            for tv in TrackValue.objects.filter(name = 'referer_keyword').values('value').annotate(e = Sum('track__session__track_count')/Count('track__session')):
                print tv['e']
