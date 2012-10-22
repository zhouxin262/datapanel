#coding=utf-8
import time
from datetime import tzinfo, timedelta, datetime

from django.core.management.base import NoArgsCommand
from django.db.models import Count

from datapanel.models import Track, Project, TrackGroupByClick
from datapanel.utils import UTC

"""
A management command for statistics
"""
class Command(NoArgsCommand):
    help = "tj"

    def handle_noargs(self, **options):
        # deal with those data by projects
        j = 0
        c = Track.objects.count()
        for p in Project.objects.filter():
            for s in p.session.all():
                prv_track = None
                for i, t in enumerate(s.track.all().order_by('id')):
                    j += 1
                    if j % 10000 == 0:
                        print j, c
                    if prv_track:
                        timelength = t.dateline - prv_track.dateline
                        if timelength.seconds > 0 and timelength.seconds < 1800:
                            prv_track.timelength = timelength.seconds
                            prv_track.save()
                    t.timelength = 0
                    t.save()
                    prv_track = t



"""
ALTER TABLE `datapanel`.`datapanel_track` ADD COLUMN `timelength` INT NOT NULL  AFTER `monthline` , ADD COLUMN `datapanel_trackcol` VARCHAR(45) NULL  AFTER `timelength` ;
"""