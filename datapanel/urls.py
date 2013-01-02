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

                       # url(r'^(?P<id>\d+)/stream/list/$', 'datapanel.views.stream.list', name='stream_list'),
                       # url(r'^(?P<id>\d+)/stream/$', 'datapanel.views.stream.stream', name='stream_stream'),
                       # url(r'^(?P<id>\d+)/stream/(?P<sid>\d+)/$', 'datapanel.views.stream.view', name='stream_view'),
                       # # url(r'^(?P<id>\d+)/funnel/$', 'datapanel.views.stream.funnel', name='stream_funnel'),

                       # url(r'^(?P<id>\d+)/condition/$', 'datapanel.views.condition.list', name='condition_list'),
                       # url(r'^(?P<id>\d+)/condition/create/$', 'datapanel.views.condition.create', name='condition_create'),
                       # url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/update/$', 'datapanel.views.condition.update', name='condition_update'),
                       # url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/delete/$', 'datapanel.views.condition.delete', name='condition_delete'),

                       # url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/$', 'datapanel.views.condition.testerlist', name='condition_testerlist'),
                       # url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/create/$', 'datapanel.views.condition.testercreate', name='condition_testercreate'),
                       # url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/(?P<tester_id>\d+)/update/$', 'datapanel.views.condition.testerupdate', name='condition_testerupdate'),
                       # url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/(?P<tester_id>\d+)/delete/$', 'datapanel.views.condition.testerdelete', name='condition_testerdelete'),
                       # url(r'^sessiontj/$', 'datapanel.views.session_tj.session_tj'),
                       )

urlpatterns += patterns('django.views.generic.simple',
                        (r'^js/(?P<key>\w+)/$', cache_page(60 * 60 * 24)(direct_to_template), {'template': 'js_template.js', 'mimetype': "application/x-javascript"}),
                        )
