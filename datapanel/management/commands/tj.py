#coding=utf-8
import time
from datetime import tzinfo, timedelta, datetime

from django.core.management.base import LabelCommand
from django.db.models import Count

from datapanel.models import Track, Project, TrackGroupByCondition, TrackGroupByValue, TrackValue

"""
A management command for statistics
"""
class Command(LabelCommand):
    help = "reset_timelength,trackgroupbyvalue"

    def handle_label(self, label, **options):
        print label,
        if label == 'reset_timelength':
            # deal with those data by projects
            c = Track.objects.filter(timelength = 0).count()
            print 'total count', c
            for t in Track.objects.filter(timelength = 0).order_by('id')[:100000]:
                if t.next_track():
                    timelength = t.next_track().dateline - t.dateline
                    if timelength.seconds < 900:
                        t.timelength = timelength.seconds + 1
                        t.save()
                else:
                    t.timelength = 0
                    t.save()

        elif label == 'trackgroupbyvalue':
            # deal with the track group by value
            c = TrackValue.objects.count()
            print 'total count', c * 4
            for i, t in enumerate(TrackValue.objects.filter().order_by('id')):
                if i % 1000 == 0:
                    print (i * 100)/c, '%'
                for datetype in ['hourline', 'dayline', 'weekline', 'monthline']:
                    tg = TrackGroupByValue.objects.get_or_create(project=t.track.session.project, datetype=datetype, name=t.name, value=t.value, dateline=time.mktime(getattr(t.track, datetype).timetuple()))
                    tg[0].increase_value()

        elif label == 'trackvalue':
            c = Track.objects.count()
            print 'total count', c
            i = 0
            for t in Track.objects.filter():
                if i % 10000 == 0:
                    print (i * 100)/c, '%\t', datetime.now()
                i += 1
                if t.param_display():
                    for k,v in t.param_display().items():
                        if k not in ('referer', ):
                            tv = TrackValue.objects.get_or_create(track=t, name=k)
                            try:
                                tv[0].value = v
                                tv[0].save()
                            except:
                                pass


