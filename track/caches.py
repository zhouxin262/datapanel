#coding=utf-8
import time
from django.core.cache import cache


def add_track(track):
    for datetype in ['hour', 'day', 'week', 'month']:
        key = '%d|%d|%d|%s' % (t.session.project.id, time.mktime(t.get_time(datetype).timetuple()), t.action.id, datetype)
        if key not in action_dict:
            action_dict[key] = 1
        else:
            action_dict[key] += 1

        if datetype != 'hour':
            for trackvalue in t.value.filter():
                if trackvalue.name != 'referrer':
                    key = '%d|%d|%s|%s|%s' % (t.session.project.id, time.mktime(t.get_time(datetype).timetuple()), trackvalue.name, trackvalue.value, datetype)
                    if key not in value_dict:
                        value_dict[key] = 1
                    else:
                        value_dict[key] += 1
