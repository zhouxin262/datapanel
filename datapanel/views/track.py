#coding=utf8
import ast
from datetime import datetime
from django.http import HttpResponse
from datapanel.utils import UTC
from datapanel.models import Project, Session, Track, Referer

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
        t = Track()
        t.session = session
        t.action = request.GET.get('t','')
        t.url = request.META.get('HTTP_REFERER','')
        t.param = request.GET.get('p','')
        t.dateline = datetime.now(UTC())
        t.set_times()
        try:
            prv_track = Track.objects.filter(session = session).order_by('-dateline')[0]
            t.step = prv_track.step+1
        except:
            t.step = 0

        prv_time = prv_track.dateline
#        now = datetime.datetime.today()
#        t.timelength = now - prv_time
        t.save()

        for datetype in ['hourline', 'dayline', 'weekline', 'monthline']:
            try:
                trackGroupByClick = TrackGroupByClick.objects.get(project = s[0].project, datetype=datetype, action=t['action'], dateline=time.mktime(t[datetype].timetuple()))
            except TrackGroupByClick.DoesNotExist:
                trackGroupByClick = TrackGroupByClick(project = s[0].project, datetype=datetype, action=t['action'], dateline=time.mktime(t[datetype].timetuple()))

        if t.param_display()['referer_parsed']:
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