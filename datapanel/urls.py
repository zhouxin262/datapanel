from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                       url(r'^$', 'datapanel.views.index', name='index'),
                       url(r'^server_info/$', 'datapanel.views.server_info', name='server_info'),
                       url(r'^t/$', 'datapanel.views.t', name='track'),

                       (r'^accounts/', include('registration.backends.default.urls')),
                       (r'^project/', include('project.urls')),
                       (r'^funnel/', include('funnel.urls')),
                       (r'^track/', include('track.urls')),
                       (r'^session/', include('session.urls')),
                       (r'^ecshop/', include('ecshop.urls')),
                       (r'^referrer/', include('referrer.urls')),
                       )

urlpatterns += patterns('django.views.generic.simple',
                        (r'^js/(?P<key>\w+)/$', cache_page(60 * 60 * 24)(direct_to_template), {'template': 'js_template.js', 'mimetype': "application/x-javascript"}),
                        )
