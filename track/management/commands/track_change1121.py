#coding=utf-8
import time
from datetime import datetime

from django.core.management.base import LabelCommand

from track.models import Track


class Command(LabelCommand):

    def handle_label(self, label, **options):
        _s = datetime.now()
        _c = Track.objects.filter(referrer_site__isnull=True).count()
        _l = _c
        while _l:
            used_time = (datetime.now() - _s).seconds
            if used_time and _c > _l:
                print _l, 'left', used_time, 'used', round(float(_l) / (float(_c - _l) / used_time), 2), 'left'

            for s in Track.objects.filter(referrer_site__isnull=True)[:100]:
                s.set_referrer(s.get_value('referrer'))
                # print s.agent_id
            _l = _l - 100
            time.sleep(1)
