import ast
import time

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

from project.models import Project
from session.models import Session


class SessionMiddleware(object):
    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)
        if not request.session.session_key:
            request.session.save()

        tmp_session_key = request.COOKIES.get(settings.TMP_SESSION_COOKIE_NAME, None)
        if tmp_session_key and Session.objects.exists(tmp_session_key):
            request.session[settings.TMP_SESSION_COOKIE_NAME] = tmp_session_key

            token = request.GET.get('k', None)
            if token and not Session.objects.get(session_key=tmp_session_key).project:
                s = Session.objects.get(session_key=tmp_session_key)
                s.project = Project.objects.get(token=token)
                s.save()

        else:
            tmp_obj = Session.objects.create_new()
            try:
                token = request.GET.get('k', None)
                project = Project.objects.get(token=token)
            except:
                project = None
            tmp_obj.permanent_session_key = request.session.session_key
            tmp_obj.project = project
            tmp_obj.ipaddress = request.META.get('REMOTE_ADDR', '0.0.0.0')
            tmp_obj.user_timezone = request.META.get('TZ', '')
            try:
                params = ast.literal_eval(request.GET.get('p', ''))
                tmp_obj.set_referrer(params['referrer'])
            except:
                pass
            tmp_obj.set_user_agent(request.META.get('HTTP_USER_AGENT', ''))
            tmp_obj.save()

            request.session[settings.TMP_SESSION_COOKIE_NAME] = tmp_obj.session_key

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
                if settings.TMP_SESSION_COOKIE_NAME in request.session:
                    response.set_cookie(settings.TMP_SESSION_COOKIE_NAME,
                                        request.session[settings.TMP_SESSION_COOKIE_NAME], max_age=None,
                                        expires=None, domain=settings.SESSION_COOKIE_DOMAIN,
                                        path=settings.SESSION_COOKIE_PATH,
                                        secure=settings.SESSION_COOKIE_SECURE or None,
                                        httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        return response


# import ast
# import time

# from django.conf import settings
# from django.utils.cache import patch_vary_headers
# from django.utils.http import cookie_date
# from django.utils.importlib import import_module

# from datapanel import tmp_session
# from project.models import Project


# class SessionMiddleware(object):
#     def process_request(self, request):
#         engine = import_module(settings.SESSION_ENGINE)
#         session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
#         request.session = engine.SessionStore(session_key)

#         if not request.session.session_key:
#             request.session.save()
#         tmp_session_key = request.COOKIES.get(settings.TMP_SESSION_COOKIE_NAME, None)
#         request.session['tmp'] = tmp_session.SessionStore(tmp_session_key)

#         if not request.session['tmp'].session_key:
#             try:
#                 token = request.GET.get('k', -1)
#                 project = Project.objects.get(token=token)
#             except:
#                 project = None

#             request.session['tmp']['permanent_session_key'] = request.session.session_key
#             request.session['tmp']['project'] = project
#             request.session['tmp']['ipaddress'] = request.META.get('REMOTE_ADDR', '0.0.0.0')
#             request.session['tmp']['user_timezone'] = request.META.get('TZ', '')
#             try:
#                 params = ast.literal_eval(request.GET.get('p', ''))
#                 request.session['tmp'].set_referrer(params['referrer'])
#             except:
#                 pass
#             request.session['tmp'].set_user_agent(request.META.get('HTTP_USER_AGENT', ''))
#             request.session['tmp'].save()

#     def process_response(self, request, response):
#         """
#         If request.session was modified, or if the configuration is to save the
#         session every time, save the changes and set a session cookie.
#         """
#         try:
#             accessed = request.session.accessed
#             modified = request.session.modified
#         except AttributeError:
#             pass
#         else:
#             if accessed:
#                 patch_vary_headers(response, ('Cookie',))
#             if modified:
#                 max_age = request.session.get_expiry_age()
#                 expires_time = time.time() + max_age
#                 expires = cookie_date(expires_time)
#                 # Save the session data and refresh the client cookie.

#                 # cross site cookie protocol
#                 response["P3P"] = "CP=CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"
#                 response.set_cookie(settings.SESSION_COOKIE_NAME,
#                                     request.session.session_key, max_age=max_age,
#                                     expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
#                                     path=settings.SESSION_COOKIE_PATH,
#                                     secure=settings.SESSION_COOKIE_SECURE or None,
#                                     httponly=settings.SESSION_COOKIE_HTTPONLY or None)
#                 request.session.save()

#         if 'tmp' in request.session:
#             try:
#                 accessed = request.session['tmp'].accessed
#                 modified = request.session['tmp'].modified
#             except AttributeError:
#                 pass
#             else:
#                 if accessed:
#                     patch_vary_headers(response, ('Cookie',))
#                 if modified:
#                     # cross site cookie protocol
#                     response["P3P"] = "CP=CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"

#                     max_age = None
#                     expires = None
#                     # Save the session data and refresh the client cookie.
#                     response.set_cookie(settings.TMP_SESSION_COOKIE_NAME,
#                                         request.session['tmp'].session_key, max_age=max_age,
#                                         expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
#                                         path=settings.SESSION_COOKIE_PATH,
#                                         secure=settings.SESSION_COOKIE_SECURE or None,
#                                         httponly=settings.SESSION_COOKIE_HTTPONLY or None)
#                     request.session['tmp'].save()
#                     print request.session['tmp'].save
#         return response
