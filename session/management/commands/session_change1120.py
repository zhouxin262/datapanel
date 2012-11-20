#coding=utf-8
from datetime import datetime

from django.core.management.base import LabelCommand

from session.models import Session, UserAgent, UserDevice, UserOS
from datapanel.ua_parser import user_agent_parser


class Command(LabelCommand):

    def handle_label(self, label, **options):
        _s = datetime.now()
        _c = Session.objects.filter().count()
        for i in range(0, _c, 3000):
            used_time = (datetime.now() - _s).seconds
            if used_time:
                print used_time, 'used', round(float(_c)/(float(i)/used_time), 2), 'left'
            for s in Session.objects.filter()[i: i + 3000]:
                parsed = user_agent_parser.Parse(s.user_agent)
                for name, obj in parsed.items():
                    T = None
                    if name == 'user_agent':
                        T = UserAgent
                        f = 'agent'
                    elif name == 'os':
                        T = UserOS
                        f = 'os'
                    elif name == 'device':
                        T = UserDevice
                        f = 'device'
                    else:
                        continue

                    args = {}
                    for k, v in obj.items():
                        if v == None:
                            v = ''
                        args[k] = v
                    try:
                        t = T.objects.get(**args)
                    except:
                        t = T()
                        for k, v in args.items():
                            setattr(t, k, v)
                        t.save()
                    setattr(s, f+'_id', t.id)
                    s.save()




