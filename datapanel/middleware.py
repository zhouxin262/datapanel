import ast
import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from datapanel import tmp_session
from project.models import Project


class SessionMiddleware(object):
    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)

        tmp_session_key = request.COOKIES.get(settings.TMP_SESSION_COOKIE_NAME, None)
        request.session['tmp'] = tmp_session.SessionStore(tmp_session_key)

        if not tmp_session_key:
            try:
                token = request.GET.get('k', -1)
                project = Project.objects.get(token=token)
                ts = request.session['tmp'].load()
                ts.project = project
                ts.ipaddress = request.META.get('REMOTE_ADDR', '0.0.0.0')
                ts.set_user_agent(request.META.get('HTTP_USER_AGENT', ''))
                ts.user_timezone = request.META.get('TZ', '')
                params = ast.literal_eval(request.GET.get('p', ''))
                ts.set_referrer(params['referrer'])
            except:
                pass

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            pass
        else:
            if accessed:
                patch_vary_headers(response, ('Cookie',))
            if modified:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)
                # Save the session data and refresh the client cookie.

                # cross site cookie protocol
                response["P3P"] = "CP=CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"
                response.set_cookie(settings.SESSION_COOKIE_NAME,
                                    request.session.session_key, max_age=max_age,
                                    expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                    path=settings.SESSION_COOKIE_PATH,
                                    secure=settings.SESSION_COOKIE_SECURE or None,
                                    httponly=settings.SESSION_COOKIE_HTTPONLY or None)
                request.session.save()

                max_age = None
                expires = None
                # Save the session data and refresh the client cookie.
                response.set_cookie(settings.TMP_SESSION_COOKIE_NAME,
                                    request.session['tmp'].session_key, max_age=max_age,
                                    expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                    path=settings.SESSION_COOKIE_PATH,
                                    secure=settings.SESSION_COOKIE_SECURE or None,
                                    httponly=settings.SESSION_COOKIE_HTTPONLY or None)
                tmp_session = request.session['tmp']
                print tmp_session
                request.session['tmp'].save()
        return response
