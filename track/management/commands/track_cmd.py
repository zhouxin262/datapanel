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

            c = Track.objects.filter(id__gt = last_id).count()
            _s = datetime.now()
            for i in range(0, c, 1000):
                # 1000 lines a time
                used_time = (datetime.now() - _s).seconds
                if used_time:
                    print i, c, used_time, '%d seconds left' % ((c-i)/(i/used_time))
                tt = Track.objects.filter(id__gt = last_id)[i: i + 1000]


                action_dict = {}
                value_dict = {}
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

        elif label == 'truncate':
            cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'trackgroup', class_name='Track')
            cmdSerialNumber[0].last_id = 0
            cmdSerialNumber[0].save()
            TrackGroupByAction.objects.filter().delete()
            TrackGroupByValue.objects.filter().delete()

        elif label == 'value':
            # deal with sogou unicode bug
            tvs = TrackValue.objects.filter(value__startswith = '%u')
            for tv in tvs:
                print tv.id
                tv.value = "".join([unichr(int(i, 16)) for i in tv.value.split('%u')[1:]])
                tv.save()

        print label, '====finished====', datetime.now()
