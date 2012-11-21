#coding=utf-8
from datetime import datetime

from django.core.management.base import LabelCommand

from session.models import Session


class Command(LabelCommand):

    def handle_label(self, label, **options):
        _s = datetime.now()
        _c = Session.objects.filter(agent__isnull=True).count()
        _l = _c
        while _l:
            used_time = (datetime.now() - _s).seconds
            if used_time:
                print used_time, 'used', round(float(_l) / (float(_c - _l) / used_time), 2), 'left'

            for s in Session.objects.filter(agent__isnull=True)[:3000]:
                s.set_user_agent(s.user_agent)
                s.set_referrer(s.user_referrer)
                # print s.agent_id

            _l = Session.objects.filter(agent__isnull=True).count()
