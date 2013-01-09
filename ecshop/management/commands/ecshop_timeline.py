#coding=utf-8
from datetime import datetime

from django.core.management.base import LabelCommand

from datapanel.models import Timeline
from track import models as track_models
from session import models as session_models

class Command(LabelCommand):

    def handle_label(self, label, **options):
        print '====started at %s====' % datetime.now()
        for modelname in ['GAction', 'GReferrerSiteAndAction', 'GReferrerKeywordAndAction']:
            TrackClass = getattr(track_models, modelname)
            for r in TrackClass.objects.filter():
                g = Timeline.objects.get_or_create(datetype=r.datetype, dateline=r.dateline)
                r.timeline = g[0]
                r.save()

        for modelname in ['GReferrerKeyword', 'GReferrerSite', 'GTime']:
            TrackClass = getattr(session_models, modelname)
            for r in TrackClass.objects.filter():
                g = Timeline.objects.get_or_create(datetype=r.datetype, dateline=r.dateline)
                r.timeline = g[0]
                r.save()

        print '====finished at %s====' % datetime.now()
