#coding=utf-8
from django.core.management.base import NoArgsCommand

from session.models import Session

"""
A management command for statistics
"""


class Command(NoArgsCommand):
    help = "funnel"

    def handle_noargs(self, **options):
        c = Session.objects.filter().count()
        for i in range(0, 30, 10):
            # 1000 lines a time
            print i, c
            ss = Session.objects.filter()[i: i + 10]
            for s in ss:
                stream = []
                for t in s.track.filter().order_by('-id'):
                    referer_tracks = s.track.filter(url=t.get_value('referer')).order_by('-id')
                    if referer_tracks:
                        stream.append((referer_tracks[0].action, t.action))

                print stream
