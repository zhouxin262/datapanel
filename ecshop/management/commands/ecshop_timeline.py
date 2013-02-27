# coding=utf-8
from datetime import datetime, timedelta

from django.core.management.base import LabelCommand

from datapanel.models import Timeline
from project.models import Project
from ecshop.models import Report1


class Command(LabelCommand):

    def handle_label(self, label, **options):
        print '====started at %s====' % datetime.now()
        for i in range(60):
            days_before = i + 1
            s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before)
            e = s + timedelta(days=1)
            print s, e
            for p in Project.objects.filter():
                timeline = Timeline.objects.get_or_create(datetype='day', dateline=s)
                Report1.objects.refresh_confirm_order(
                    project=p, timeline=timeline[0], start_dateline=s, end_dateline=e)

        print '====finished at %s====' % datetime.now()
