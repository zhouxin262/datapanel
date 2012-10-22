from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', 'datapanel.views.index', name='index'),
    url(r'^server_info/$', 'datapanel.views.server_info', name='server_info'),
    url(r'^track/$', 'datapanel.views.track.default', name='track'),

    url(r'^create/$', 'datapanel.views.project.create', name='project_create'),
    url(r'^(?P<id>\d+)/$', 'datapanel.views.project.home', name='project_home'),
    url(r'^(?P<id>\d+)/delete/$', 'datapanel.views.project.delete', name='project_delete'),
    url(r'^(?P<id>\d+)/setting/$', 'datapanel.views.project.setting', name='project_setting'),

    url(r'^(?P<id>\d+)/stream/$', 'datapanel.views.stream.list', name='stream_list'),
    url(r'^(?P<id>\d+)/stream/(?P<sid>\d+)/$', 'datapanel.views.stream.view', name='stream_view'),
    url(r'^(?P<id>\d+)/referer/$', 'datapanel.views.stream.referer_list', name='referer_list'),

    url(r'^(?P<id>\d+)/group/$', 'datapanel.views.group.home', name='group_home'),

    (r'^accounts/', include('registration.backends.default.urls')),

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
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^js/(?P<key>\w+)/$', 'direct_to_template', {'template': 'js_template.js', 'mimetype': "application/javascript"}),
)