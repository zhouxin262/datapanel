#coding=utf-8
from datetime import datetime

from django.core.management.base import LabelCommand

from datapanel.models import Timeline
from ecshop.models import Report1
from track.models import GAction


class Command(LabelCommand):

    def handle_label(self, label, **options):
        print '====started at %s====' % datetime.now()
        for r in Report1.objects.filter():
            g = Timeline.objects.get_or_create(datetype=r.datetype, dateline=r.dateline)
            r.timeline = g[0]
            r.save()

        for r in GAction.objects.filter():
            g = Timeline.objects.get_or_create(datetype=r.datetype, dateline=r.dateline)

        print '====finished at %s====' % datetime.now()
