#coding=utf-8
import time
from datetime import datetime
from django.core.management.base import LabelCommand

from session.models import Session
from track.models import Track, TrackValue, TrackGroupByAction, TrackGroupByValue
from datapanel.models import CmdSerialNumber

"""
A management command for statistics
"""


class Command(LabelCommand):
    help = "byaction"

    def handle_label(self, label, **options):
        print label, '====started====', datetime.now()
        if label == 'group':
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'trackgroup', class_name='Track')
            last_id = cmdSerialNumber[0].last_id

            action_dict = {}
            value_dict = {}
            c = Track.objects.filter(id__gt = last_id).count()
            _s = datetime.now()
            for i in range(0, c, 1000):
                # 1000 lines a time
                used_time = (datetime.now() - _s).seconds
                if used_time:
                    print i, c, used_time, '%d seconds left' % ((c-i)/(i/used_time))
                tt = Track.objects.filter(id__gt = last_id)[i: i + 1000]
                for t in tt:
                    for datetype in ['hour', 'day', 'week', 'month']:
                        key = '%d|%d|%d|%s' % (t.session.project.id, time.mktime(t.get_time(datetype).timetuple()), t.action.id, datetype)
                        if key not in action_dict:
                            action_dict[key] = 1
                        else:
                            action_dict[key] += 1

                        if datetype != 'hour':
                            for trackvalue in t.value.filter():
                                if trackvalue.name != 'referer':
                                    key = '%d|%d|%s|%s|%s' % (t.session.project.id, time.mktime(t.get_time(datetype).timetuple()), trackvalue.name, trackvalue.value, datetype)
                                    if key not in value_dict:
                                        value_dict[key] = 1
                                    else:
                                        value_dict[key] += 1

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

            # update the last_id which has been grouped
            cmdSerialNumber[0].last_id = t.id
            cmdSerialNumber[0].save()


        elif label == 'value':
            c = Session.objects.filter().count()
            _s = datetime.now()
            for i in range(0, c, 1000):
                # 1000 lines a time
                used_time = (datetime.now() - _s).seconds
                print i, c, used_time
                ss = Session.objects.filter()[i: i + 1000]

                for s in ss:
                    for t in s.track.filter().order_by('id'):
                        if t.param_display():
                            for k, v in t.param_display().items():
                                try:
                                    TrackValue(track=t, name=k, value=v).save()
                                except:
                                    print t.id

        print label, '====finished====', datetime.now()
