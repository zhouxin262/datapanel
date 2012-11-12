#coding=utf-8
import time
from datetime import datetime, timedelta
from django.core.management.base import LabelCommand
from django.db.models import Count

from project.models import Project
from session.models import Session
from track.models import Track, TrackValue, TrackGroupByAction, TrackGroupByValue
from datapanel.models import CmdSerialNumber

"""
A management command for statistics
"""


class Command(LabelCommand):
    help = "byaction"
    command_name = "track_cmd"
    label = ""

    def hour_update(self):
        # hour
        _s = datetime.now()

        cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name='%s %s' % (self.command_name, self.label), class_name='Track')
        last_id = cmdSerialNumber[0].last_id

        last_time = None
        try:
            last_time = Track.objects.get(id=last_id).dateline
        except:
            last_time = Track.objects.filter().order_by('dateline')[0].dateline

        if last_time:
            total_hour = (datetime.now() - last_time).days * 24 + (datetime.now() - last_time).seconds / 3600
            last_hour = (last_time).replace(minute=0, second=0, microsecond=0)
            for hour_step in range(total_hour + 1):
                # print time used
                used_time = (datetime.now() - _s).seconds
                if used_time > 0 and hour_step > 0 and float(hour_step) / used_time > 0:
                    print hour_step, total_hour, used_time, '%d seconds left' % (float(total_hour - hour_step) / (float(hour_step) / used_time))

                # get time range
                s = last_hour
                e = last_hour + timedelta(seconds=3600)
                dateline = time.mktime(s.timetuple())

                # clean db
                TrackGroupByAction.objects.filter(dateline=dateline, datetype='hour').delete()
                TrackGroupByValue.objects.filter(dateline=dateline, datetype='hour').delete()

                # filter track by time
                track_list = Track.objects.filter(dateline__range=[s, e])
                trackvalue_list = TrackValue.objects.filter(track__dateline__range=[s, e])

                for p in Project.objects.filter():
                    # group by track action
                    dataset = track_list.filter(session__project=p).values('action').annotate(c=Count('action'))
                    data = []
                    for datarow in dataset:
                        ta = TrackGroupByAction()
                        ta.project = p
                        ta.datetype = 'hour'
                        ta.dateline = dateline
                        ta.action_id = datarow['action']
                        ta.count = datarow['c']
                        data.append(ta)

                    # insert into db
                    TrackGroupByAction.objects.bulk_create(data)

                    # group by track value
                    dataset = trackvalue_list.filter(track__session__project=p).values('name', 'value').annotate(c=Count('value'))
                    data = []
                    for datarow in dataset:
                        if len(datarow['value']) < 30:
                            tv = TrackGroupByValue()
                            tv.project = p
                            tv.datetype = 'hour'
                            tv.dateline = dateline
                            tv.name = datarow['name']
                            tv.value = datarow['value']
                            tv.count = datarow['c']
                            data.append(tv)

                    # insert into db
                    TrackGroupByValue.objects.bulk_create(data)
                    last_hour = e

    def handle_label(self, label, **options):
        self.label = label
        print label, '====started====', datetime.now()
        if label == 'hourupdate':
            self.hour_update()

        elif label == 'update':
            # day

            # week

            # month
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name='trackgroup', class_name='Track')
            last_id = cmdSerialNumber[0].last_id

            c = Track.objects.filter(id__gt=last_id).count()
            _s = datetime.now()
            print c
            for i in range(0, c, 1000):
                # 3000 lines a time
                used_time = (datetime.now() - _s).seconds
                if used_time:
                    print i, c, used_time, '%d seconds left' % ((c - i) / (i / used_time))
                tt = Track.objects.filter(id__gt=last_id)[i: i + 1000]

                action_dict = {}
                value_dict = {}
                for t in tt:
                    for datetype in ['hour', 'day', 'week', 'month']:
                        key = '%d|%d|%d|%s' % (t.session.project.id, time.mktime(t.get_time(datetype).timetuple()), t.action.id, datetype)
                        if key not in action_dict:
                            action_dict[key] = 1
                        else:
                            action_dict[key] += 1

                    for datetype in ['day', 'week', 'month']:
                        for trackvalue in t.value.filter():
                            if trackvalue.name != 'referer' and len(trackvalue.value) < 30:
                                key = '%d|%d|%s|%s|%s' % (t.session.project.id, time.mktime(t.get_time(datetype).timetuple()), trackvalue.name, trackvalue.value, datetype)
                                if key not in value_dict:
                                    value_dict[key] = 1
                                else:
                                    value_dict[key] += 1

                print (datetime.now() - _s).seconds, len(value_dict.keys())
                # update the last_id whiv ch has been grouped
                cmdSerialNumber[0].last_id = t.id
                cmdSerialNumber[0].save()

                for k, v in action_dict.items():
                    project_id = k.split("|")[0]
                    dateline = k.split("|")[1]
                    action_id = k.split("|")[2]
                    datetype = k.split("|")[3]
                    ta = TrackGroupByAction.objects.get_or_create(project_id=project_id,
                                                                  datetype=datetype,
                                                                  action_id=action_id,
                                                                  dateline=dateline)
                    ta[0].count += v
                    ta[0].save()

                print (datetime.now() - _s).seconds
                for k, v in value_dict.items():
                    project_id = k.split("|")[0]
                    dateline = k.split("|")[1]
                    name = k.split("|")[2]
                    value = k.split("|")[3]
                    datetype = k.split("|")[4]
                    tv = TrackGroupByValue.objects.get_or_create(project_id=project_id,
                                                                 datetype=datetype,
                                                                 name=name,
                                                                 value=value,
                                                                 dateline=dateline)
                    tv[0].count += v
                    tv[0].save()
                print (datetime.now() - _s).seconds

        elif label == 'truncate':
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name='trackgroup', class_name='Track')
            cmdSerialNumber[0].last_id = 0
            cmdSerialNumber[0].save()
            TrackGroupByAction.objects.filter().delete()
            TrackGroupByValue.objects.filter().delete()

        elif label == 'keeprecent':
            print 'session: ', Session.objects.filter().count()
            print 'track: ', Track.objects.filter().count()
            now = datetime.now()

            c = 1
            i = 2
            while c > 0:
                s = now - timedelta(days=i + 1)
                e = now - timedelta(days=i)
                i += 1
                c = Session.objects.filter(start_time__range=[s, e]).count()
                print 'find session in', s, e
                if c:
                    print c, ' session deleting'
                    Session.objects.filter(start_time__range=[s, e]).delete()
                    print c, ' session deleted'

            print 'left session: ', Session.objects.filter().count()
            print 'left track: ', Track.objects.filter().count()

        elif label == 'value':
            # deal with sogou unicode bug
            tvs = TrackValue.objects.filter(value__startswith='%u')
            for tv in tvs:
                print tv.id
                tv.value = "".join([unichr(int(i, 16)) for i in tv.value.split('%u')[1:]])
                tv.save()

        else:
            print 'wrong label'

        print label, '====finished====', datetime.now()
