from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'datapanel.views.index', name='index'),
                       url(r'^server_info/$', 'datapanel.views.server_info', name='server_info'),
                       url(r'^t/$', 'datapanel.views.t', name='track'),

                       (r'^accounts/', include('registration.backends.default.urls')),
                       (r'^project/', include('project.urls')),
                       (r'^funnel/', include('funnel.urls')),
                       (r'^track/', include('track.urls')),
                       (r'^session/', include('session.urls')),

                       # url(r'^(?P<id>\d+)/stream/list/$', 'datapanel.views.stream.list', name='stream_list'),
                       # url(r'^(?P<id>\d+)/stream/$', 'datapanel.views.stream.stream', name='stream_stream'),
                       # url(r'^(?P<id>\d+)/stream/(?P<sid>\d+)/$', 'datapanel.views.stream.view', name='stream_view'),
<<<<<<< HEAD
                       url(r'^(?P<id>\d+)/track/groupby_value/$', 'datapanel.views.track.groupby_value', name='track_groupby_value'),
                       url(r'^(?P<id>\d+)/track/groupby_action/$', 'datapanel.views.track.groupby_action', name='track_groupby_action'),
                       url(r'^(?P<id>\d+)/track/groupby_referer/$', 'datapanel.views.track.groupby_referer', name='track_groupby_referer'),
                       url(r'^(?P<id>\d+)/track/get_url_by_value/$', 'datapanel.views.track.get_url_by_value', name='track_get_url_by_value'),
                       url(r'^(?P<id>\d+)/track/get_referer_url/$', 'datapanel.views.track.get_referer_url', name='track_get_referer_url'),

                       url(r'^(?P<id>\d+)/stream/list/$', 'datapanel.views.stream.list', name='stream_list'),
                       url(r'^(?P<id>\d+)/stream/$', 'datapanel.views.stream.stream', name='stream_stream'),
                       url(r'^(?P<id>\d+)/stream/(?P<sid>\d+)/$', 'datapanel.views.stream.view', name='stream_view'),
                       # url(r'^(?P<id>\d+)/funnel/$', 'datapanel.views.stream.funnel', name='stream_funnel'),

                       url(r'^(?P<id>\d+)/action/$', 'datapanel.views.action.list', name='action_list'),
                       url(r'^(?P<id>\d+)/action/create/$', 'datapanel.views.action.create', name='action_create'),
                       url(r'^(?P<id>\d+)/action/(?P<aid>\d+)/update/$', 'datapanel.views.action.update', name='action_update'),
                       url(r'^(?P<id>\d+)/action/(?P<aid>\d+)/delete/$', 'datapanel.views.action.delete', name='action_delete'),

                       url(r'^(?P<id>\d+)/condition/$', 'datapanel.views.condition.list', name='condition_list'),
                       url(r'^(?P<id>\d+)/condition/create/$', 'datapanel.views.condition.create', name='condition_create'),
                       url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/update/$', 'datapanel.views.condition.update', name='condition_update'),
                       url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/delete/$', 'datapanel.views.condition.delete', name='condition_delete'),

                       url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/$', 'datapanel.views.condition.testerlist', name='condition_testerlist'),
                       url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/create/$', 'datapanel.views.condition.testercreate', name='condition_testercreate'),
                       url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/(?P<tester_id>\d+)/update/$', 'datapanel.views.condition.testerupdate', name='condition_testerupdate'),
                       url(r'^(?P<id>\d+)/condition/(?P<condition_id>\d+)/tester/(?P<tester_id>\d+)/delete/$', 'datapanel.views.condition.testerdelete', name='condition_testerdelete'),
=======
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
>>>>>>> origin/0.1
                       )

urlpatterns += patterns('django.views.generic.simple',
                        (r'^js/(?P<key>\w+)/$', 'direct_to_template', {'template': 'js_template.js', 'mimetype': "application/javascript"}),
                        )
