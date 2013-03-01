import ast
import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from project.models import Project
from session.models import Session
from datapanel.views import analysis, get_and_verify_data


class SessionMiddleware(object):
    def should_process(self, request):
        if getattr(settings, 'STATIC_URL', None) and request.build_absolute_uri().startswith(request.build_absolute_uri(settings.STATIC_URL)):
            return False
        if settings.MEDIA_URL and request.build_absolute_uri().startswith(request.build_absolute_uri(settings.MEDIA_URL)):
            return False
        if getattr(settings, 'ADMIN_MEDIA_PREFIX', None) and request.path.startswith(settings.ADMIN_MEDIA_PREFIX):
            return False
        if request.path == '/favicon.ico':
            return False
        for path in getattr(settings, 'DEVSERVER_IGNORED_PREFIXES', []):
            if request.path.startswith(path):
                return False
        return True

    def process_request(self, request):
        if self.should_process(request):
            engine = import_module(settings.SESSION_ENGINE)
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
            request.session = engine.SessionStore(session_key)

            tmp_session_key = request.COOKIES.get(settings.TMP_SESSION_COOKIE_NAME, None)

            if tmp_session_key and Session.objects.exists(tmp_session_key) and \
                    settings.TMP_SESSION_COOKIE_NAME in request.session:
                if not tmp_session_key == request.session[settings.TMP_SESSION_COOKIE_NAME]:
                    request.session[settings.TMP_SESSION_COOKIE_NAME] = tmp_session_key
            else:
                request.session[settings.TMP_SESSION_COOKIE_NAME] = None

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        if self.should_process(request):
            try:
                accessed = request.session.accessed
                modified = request.session.modified
            except AttributeError:
                pass
            else:
                if accessed:
                    patch_vary_headers(response, ('Cookie',))
                if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                    if request.session.get_expire_at_browser_close():
                        max_age = None
                        expires = None
                    else:
                        max_age = request.session.get_expiry_age()
                        expires_time = time.time() + max_age
                        expires = cookie_date(expires_time)
                    # Save the session data and refresh the client cookie.
                    request.session.save()
                    response["P3P"] = "CP=CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"
                    response.set_cookie(settings.SESSION_COOKIE_NAME,
                                        request.session.session_key, max_age=max_age,
                                        expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                                        path=settings.SESSION_COOKIE_PATH,
                                        secure=settings.SESSION_COOKIE_SECURE or None,
                                        httponly=settings.SESSION_COOKIE_HTTPONLY or None)

                    if not (settings.TMP_SESSION_COOKIE_NAME in request.session and request.session[settings.TMP_SESSION_COOKIE_NAME]):
                        # processing data
                        (is_verified, data) = get_and_verify_data(request)
                        if is_verified:
                            # create temp session key, refresh everytime when users close their browser.
                                token = data.get('k')
                                project = Project.objects.get(token=token)
                                tmp_obj = Session.objects.create_new(project)
                                tmp_obj.project = project
                                tmp_obj.permanent_session_key = request.session.session_key
                                tmp_obj.ipaddress = request.META.get('REMOTE_ADDR', '0.0.0.0')
                                tmp_obj.user_timezone = request.META.get('TZ', '')
                                tmp_obj.set_user_agent(request.META.get('HTTP_USER_AGENT', ''))
                                tmp_obj.set_referrer(data.get('r'))
                                tmp_obj.save()

                                request.session[settings.TMP_SESSION_COOKIE_NAME] = tmp_obj.session_key
                                response.set_cookie(settings.TMP_SESSION_COOKIE_NAME,
                                                    request.session[settings.TMP_SESSION_COOKIE_NAME], max_age=None,
                                                    expires=None, domain=settings.SESSION_COOKIE_DOMAIN,
                                                    path=settings.SESSION_COOKIE_PATH,
                                                    secure=settings.SESSION_COOKIE_SECURE or None,
                                                    httponly=settings.SESSION_COOKIE_HTTPONLY or None)
            if request.path == '/a/':
                analysis(request, response)
        return response
