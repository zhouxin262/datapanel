# coding=utf-8
from django.core.management.base import NoArgsCommand
from django.core.cache import cache


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        cache.clear()
