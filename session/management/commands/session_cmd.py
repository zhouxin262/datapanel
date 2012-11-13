#coding=utf-8
import os, sys
from django.db.models import Max
from datetime import datetime
from django.core.management.base import NoArgsCommand, LabelCommand
from datapanel.models import CmdSerialNumber
from project.models import Project
from session.models import SessionGroupByTime, Session


class Command(LabelCommand):

    def handle_label(self, label, **options):
        if label == 'groupbytime':
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'sessiongroupbytime', class_name='Session')
            last_id = cmdSerialNumber[0].last_id
            projects = Project.objects.all()
            for project in projects:

                c = Session.objects.filter(id__gt = last_id).count()
                _s = datetime.now()
                for i in range(0, c, 3000):
                # 3000 lines a time
                    used_time = (datetime.now() - _s).seconds
                    if used_time:
                        print i, c, used_time, '%d seconds left' % ((c-i)/(i/used_time))
                    sessions = Session.objects.filter(project = project,id__gt = last_id)[i: i + 3000]
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

        elif label == 'truncate':
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'sessiongroupbytime', class_name='Session')
            cmdSerialNumber[0].last_id = 0
            cmdSerialNumber[0].save()
            SessionGroupByTime.objects.all().delete()

        elif label == 'referer':
            c = Session.objects.filter(user_referer_keyword='').order_by('id').count()
            _s = datetime.now()

            for i in range(0, c, 3000):
            # 3000 lines a time
                used_time = (datetime.now() - _s).seconds
                if used_time:
                    print i, c, used_time, '%d seconds left' % ((c-i)/(i/used_time))

                for s in Session.objects.filter(user_referer_keyword='').order_by('id')[i:i+3000]:
                    if s.first_track():
                        s.user_referer_keyword = s.first_track().get_value('referer_keyword')
                        s.user_referer_site = s.first_track().get_value('referer_site')
                        s.user_referer = s.first_track().get_value('referer')
                        s.save()
                    else:
                        s.delete()
                    #s.save()
