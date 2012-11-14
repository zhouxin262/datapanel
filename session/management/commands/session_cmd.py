#coding=utf-8
import time
from datetime import datetime, timedelta

from django.db.models import Max, Count, Sum
from django.core.management.base import NoArgsCommand, LabelCommand

from datapanel.models import CmdSerialNumber
from project.models import Project
from session.models import GTime, Session, GReferrerKeyword, GReferrerSite


class Command(LabelCommand):

    def handle_label(self, label, **options):
        days_before = 0
        try:
            days_before = int(label)
        except:
            print 'wrong label, should be int'
            return None

        _s = datetime.now()

        """
        group by time per hour
        """
        for i in range(24):
            used_time = (datetime.now() - _s).seconds
            if used_time > 0:
                print used_time, 'seconds used', '%d seconds left' % (float(23 - i) / (float(i) / used_time))

            # print i,

            # get time range
            s = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
            e = s + timedelta(seconds=3600)
            dateline = time.mktime(s.timetuple())

            # clean db
            GTime.objects.filter(dateline=dateline, datetype='hour').delete()
            GReferrerSite.objects.filter(dateline=dateline, datetype='hour').delete()
            GReferrerKeyword.objects.filter(dateline=dateline, datetype='hour').delete()

            # filter track by time
            session_list = Session.objects.filter(start_time__range=[s, e])

            if session_list:
                # foreach project
                for p in Project.objects.filter():
                    # group by time
                    dataset = session_list.filter(project=p).aggregate(c=Count('id'),s=Sum('track_count'))
                    gt = GTime()
                    gt.project = p
                    gt.datetype = 'hour'
                    gt.dateline = dateline
                    gt.count = dataset['c']
                    gt.track_count = dataset['s']
                    gt.save()

                    # group by user_referrer_site and time
                    dataset = session_list.filter(project=p).exclude(user_referrer_site='').values('user_referrer_site').annotate(c=Count('user_referrer_site'),
                                                                                              s=Sum('track_count'))
                    data = []
                    for datarow in dataset:
                        ta = GReferrerSite()
                        ta.project = p
                        ta.datetype = 'hour'
                        ta.dateline = dateline
                        ta.value = datarow['user_referrer_site']
                        ta.count = datarow['c']
                        ta.track_count = datarow['s']
                        data.append(ta)

                    # insert into db
                    GReferrerSite.objects.bulk_create(data)

                    # group by user_referrer_keyword and time
                    dataset = session_list.filter(project=p).exclude(user_referrer_keyword='').values('user_referrer_keyword').annotate(c=Count('user_referrer_keyword'),
                                                                                              s=Sum('track_count'))
                    data = []
                    for datarow in dataset:
                        ta = GReferrerSite()
                        ta.project = p
                        ta.datetype = 'hour'
                        ta.dateline = dateline
                        ta.value = datarow['user_referrer_keyword']
                        ta.count = datarow['c']
                        ta.track_count = datarow['s']
                        data.append(ta)

                    # insert into db
                    GReferrerKeyword.objects.bulk_create(data)

        """
        group by time per day
        """
        # all day data
        s = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_before + 1)
        e = s + timedelta(days=1)
        dateline = time.mktime(s.timetuple())
        e_timestamp = time.mktime(e.timetuple())

        # clean db
        GTime.objects.filter(dateline=dateline, datetype='day').delete()
        GReferrerSite.objects.filter(dateline=dateline, datetype='day').delete()
        GReferrerKeyword.objects.filter(dateline=dateline, datetype='day').delete()

        # foreach projects
        for p in Project.objects.filter():
            # group by time
            dataset = GTime.objects.filter(dateline__range=[dateline, e_timestamp], project=p).aggregate(c=Sum('count'),s=Sum('track_count'))
            gt = GTime()
            gt.project = p
            gt.datetype = 'day'
            gt.dateline = dateline
            gt.count = dataset['c']
            gt.track_count = dataset['s']
            gt.save()

            # group by user_referrer_site and time
            dataset = [datarow for datarow in GReferrerSite.objects.filter(dateline__range=[dateline, e_timestamp], project=p).values('value').annotate(c=Sum('count'),s=Sum('track_count'))]
            data = []
            for datarow in dataset:
                ta = GReferrerSite()
                ta.project = p
                ta.datetype = 'day'
                ta.dateline = dateline
                ta.value = datarow['value']
                ta.count = datarow['c']
                ta.track_count = datarow['s']
                data.append(ta)

            # insert into db
            GReferrerSite.objects.bulk_create(data)

            # group by user_referrer_site and time
            dataset = [datarow for datarow in GReferrerKeyword.objects.filter(dateline__range=[dateline, e_timestamp], project=p).values('value').annotate(c=Sum('count'),s=Sum('track_count'))]
            data = []
            for datarow in dataset:
                ta = GReferrerKeyword()
                ta.project = p
                ta.datetype = 'day'
                ta.dateline = dateline
                ta.value = datarow['value']
                ta.count = datarow['c']
                ta.track_count = datarow['s']
                data.append(ta)

            # insert into db
            GReferrerKeyword.objects.bulk_create(data)

        print label, '====finished====', datetime.now()
