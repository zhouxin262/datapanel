#coding=utf8
import ast, time
from datetime import datetime
from django.http import HttpResponse
from datapanel.utils import UTC
from datapanel.models import Project, Session, Track, Referer, TrackCondition, TrackGroupByClick, Action

def get_or_create_session(request):
    token = request.GET.get('k', -1)
    # 客户服务器访问，可带客户的客户session_key
    session_key = None
    if request.GET.get('s', None):
        session_key = request.GET.get('s')
    else:
        session_key = request.session.session_key
    p = Project.objects.get(token = token)
    s = Session.objects.get_or_create(sn = session_key,
        project=p)
    if s[1]:
        s[0].ipaddress = request.META.get('REMOTE_ADDR','0.0.0.0')
        s[0].user_agent = request.META.get('HTTP_USER_AGENT','')
        s[0].user_timezone = request.META.get('TZ','')
        s[0].save()
    return s

def default(request):
    if not request.session.session_key:
        request.session.flush()
        request.session.save()

    s = get_or_create_session(request)

    if request.GET.get('t',''):
        session = s[0]
        # filter actions
        try:
            prv_track = Track.objects.filter(session = session).order_by('-dateline')[0]
            if prv_track.url == request.META.get('HTTP_REFERER',''):
                # f5 refresh
                return HttpResponse('', mimetype="application/javascript")
        except IndexError:
            prv_track = None

        try:
            a = Action.objects.get(name = request.GET.get('t', ''))
        except Action.DoesNotExist:
            return HttpResponse('', mimetype="application/javascript")

        t = Track()
        t.session = session
        t.action = request.GET.get('t','')
        t.url = request.META.get('HTTP_REFERER','')
        t.param = request.GET.get('p','')
        t.dateline = datetime.now(UTC())
        t.set_times()
        # set step
        if prv_track:
            t.step = prv_track.step+1
        else:
            t.step = 1
        # todo : set timelength
        t.save()

        for datetype in ['hourline', 'dayline', 'weekline', 'monthline']:
            conditions = TrackCondition.objects.filter(project = session.project)
            print conditions
            for i, condition in enumerate(conditions):
                test_result = None
                for tester in condition.tester.all():
                    result = False
                    if tester.test_operator == 'gt':
                        result = getattr(t, tester.col_name) > int(tester.test_value)
                    elif tester.test_operator == 'eq':
                        result = getattr(t, tester.col_name) == int(tester.test_value)
                    elif tester.test_operator == 'lt':
                        result = getattr(t, tester.col_name) < int(tester.test_value)

                    if i == 0:
                        test_result = result
                    if tester.operator == "AND":
                        test_result = test_result and result
                    else:
                        test_result = test_result or result
                    print
                print condition.id, test_result
                if test_result:
                    trackGroupByClick = TrackGroupByClick.objects.get_or_create(project = s[0].project, datetype=datetype, action=t.action, dateline=time.mktime(getattr(t, datetype).timetuple()), condition = condition)
                    trackGroupByClick[0].increase_value()

            trackGroupByClick = TrackGroupByClick.objects.get_or_create(project = s[0].project, datetype=datetype, action=t.action, dateline=time.mktime(getattr(t, datetype).timetuple()), condition=None)
            trackGroupByClick[0].increase_value()
        # deal with referer
        if t.param_display().has_key('referer_parsed'):
            r = Referer()
            r.session = session
            r.site = t.param_display()['referer_site']
            r.keyword = t.param_display()['referer_keyword']
            r.url = t.param_display()['referer']
            r.save()

    if request.GET.get('p', ''):
        params = ast.literal_eval(request.GET.get('p', ''))
        if params.has_key('function') and params['function']:
            f = params['function']
            if f[0] == 'set_user':
                s[0].username = f[1]['username']
                s[0].save()

    if s[1]:
        # 新开的session，在客户服务器上存一个，需要配合
        response_data = 'jx.callback({mp_act:"set_session", mb_session_key: "%s"});' % s[0].sn;
        return HttpResponse(response_data, mimetype="application/javascript")
    return HttpResponse('', mimetype="application/javascript")