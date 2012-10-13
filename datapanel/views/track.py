#coding=utf8
def default(request):
    if not request.session.session_key:
        request.session.flush()
        request.session.save()
        request.session.modified = False
    s = get_or_create_session(request)

    if request.GET.get('t',''):
        session = s[0]
        t = Track()
        t.session = session
        t.action = request.GET.get('t','')
        t.url = request.META.get('HTTP_REFERER','')
        t.param = request.GET.get('p','')
        t.set_times()
        t.save()

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