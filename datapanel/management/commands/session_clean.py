#coding=utf-8
from django.core.management.base import NoArgsCommand

from django.contrib.sessions.models import Session as DjangoSession
from session.models import Session

class Command(NoArgsCommand):
    def handle(self, *args, **options):
        for s in DjangoSession.objects.filter():
            print s.session_key
            if not Session.objects.filter(permanent_session_key = s.session_key):
                s.delete()
