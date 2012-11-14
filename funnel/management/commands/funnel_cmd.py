#coding=utf-8
from datetime import datetime

from django.core.management.base import NoArgsCommand

from datapanel.models import CmdSerialNumber
from track.models import Track
from funnel.models import Swipe

"""
A management command for statistics
"""


class Command(NoArgsCommand):
    help = "funnel"

    def handle_noargs(self, **options):
        print 'funnel', '====started====', datetime.now()
        cmdSerialNumber = CmdSerialNumber.objects.get_or_create(name = 'swipe', class_name='Track')
        last_id = cmdSerialNumber[0].last_id
        # last_id = 0

        c = Track.objects.filter(id__gt = last_id).count()
        _s = datetime.now()
        for i in range(0, c, 1000):
            # 1000 lines a time
            used_time = (datetime.now() - _s).seconds
            if used_time:
                print i, 'of', c, used_time, 'seconds already used', ', and %d seconds left' % ((c-i)/(i/used_time))
            tt = Track.objects.filter(id__gt = last_id)[i: i + 1000]
            swipes = []
            for t in tt:
                try:
                    probably_from_tracks = t.session.track.filter(id__lt=t.id,
                        url=t.get_value('referrer')).order_by('id')
                    if not probably_from_tracks:
                        probably_from_tracks = t.session.track.filter(id__lt=t.id).order_by('-id')
                    probably_from_track = probably_from_tracks[0]
                    swipe = Swipe()
                    swipe.project = t.session.project
                    swipe.session = t.session
                    swipe.from_action = probably_from_track.action
                    swipe.action = t.action
                    swipe.from_track = probably_from_track
                    swipe.track = t
                    swipe.dateline = t.dateline
                    swipes.append(swipe)
                except IndexError:
                     pass
            Swipe.objects.bulk_create(swipes)
            # update the last_id which has been grouped
            cmdSerialNumber[0].last_id = t.id
            cmdSerialNumber[0].save()
        print 'funnel', '====finished====', datetime.now()
