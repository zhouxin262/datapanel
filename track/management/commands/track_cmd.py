#coding=utf-8
import time
from datetime import datetime, timedelta
from django.core.management.base import LabelCommand
from django.db.models import Count, Sum

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

    def handle_label(self, label, **options):
        self.label = label
        print label, '====started====', datetime.now()

        if label == 'truncate':
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

        elif label == 'time':
            # deal with sogou unicode bug
            ts = [t for t in Track.objects.filter(timelength = 0)]
            _s = datetime.now()
            c = Track.objects.filter(timelength = 0).count()
            for i, t in enumerate(ts):
                used_time = (datetime.now() - _s).seconds
                if used_time > 0 and used_time % 10 == 0:
                    print used_time, 'seconds used', '%d seconds left' % (float(c) / (float(i+1) / used_time))

                t.set_from_track()
                t.set_prev_timelength()

        else:
            days_before = 0
            try:
                days_before = int(label)
            except:
                print 'wrong label, should be int'
                return None

            _s = datetime.now()

            for i in range(24):
                used_time = (datetime.now() - _s).seconds
                if used_time > 0:
                    print used_time, 'seconds used', '%d seconds left' % (float(23 - i) / (float(i) / used_time))

                # get time range
                s = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
                e = s + timedelta(seconds=3600)
                dateline = time.mktime(s.timetuple())

                # clean db
                TrackGroupByAction.objects.filter(dateline=dateline, datetype='hour').delete()
                TrackGroupByValue.objects.filter(dateline=dateline, datetype='hour').delete()

                # filter track by time
                track_list = Track.objects.filter(dateline__range=[s, e])
                trackvalue_list = TrackValue.objects.filter(track__dateline__range=[s, e])

                if track_list:
                    # foreach project
                    for p in Project.objects.filter():
                        # group by track action
                        dataset = track_list.filter(session__project=p).values('action').annotate(c=Count('action'), s=Sum('timelength'))
                        data = []
                        for datarow in dataset:
                            ta = TrackGroupByAction()
                            ta.project = p
                            ta.datetype = 'hour'
                            ta.dateline = dateline
                            ta.action_id = datarow['action']
                            ta.count = datarow['c']
                            ta.timelength = datarow['s']
                            data.append(ta)

                        # insert into db
                        TrackGroupByAction.objects.bulk_create(data)

                        # group by track value
                        dataset = trackvalue_list.filter(track__session__project=p).values('name', 'value').annotate(c=Count('value'), s=Sum('track__timelength'))
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
                                tv.timelength = datarow['s']
                                data.append(tv)

                        # insert into db
                        TrackGroupByValue.objects.bulk_create(data)

            # all day data
            s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
            e = s + timedelta(days=1)
            dateline = time.mktime(s.timetuple())
            e_timestamp = time.mktime(e.timetuple())

            # clean db
            TrackGroupByAction.objects.filter(dateline=dateline, datetype='day').delete()
            TrackGroupByValue.objects.filter(dateline=dateline, datetype='day').delete()

            # foreach projects
            for p in Project.objects.filter():
                # group by track action
                dataset = [datarow for datarow in TrackGroupByAction.objects.filter(dateline__range=[dateline, e_timestamp], project=p).values('action').annotate(c=Sum('count'), s=Sum('timelength'))]
                data = []
                for datarow in dataset:
                    ta = TrackGroupByAction()
                    ta.project = p
                    ta.datetype = 'day'
                    ta.dateline = dateline
                    ta.action_id = datarow['action']
                    ta.count = datarow['c']
                    tv.timelength = datarow['s']
                    data.append(ta)

                # insert into db
                TrackGroupByAction.objects.bulk_create(data)

                # group by track value
                dataset = [datarow for datarow in TrackGroupByValue.objects.filter(dateline__range=[dateline, e_timestamp], project=p).values('name', 'value').annotate(c=Sum('count'), s=Sum('timelength'))]
                data = []
                for datarow in dataset:
                    if len(datarow['value']) < 30:
                        tv = TrackGroupByValue()
                        tv.project = p
                        tv.datetype = 'day'
                        tv.dateline = dateline
                        tv.name = datarow['name']
                        tv.value = datarow['value']
                        tv.count = datarow['c']
                        tv.timelength = datarow['s']
                        data.append(tv)

                # insert into db
                TrackGroupByValue.objects.bulk_create(data)

        print label, '====finished====', datetime.now()
