from django.conf.urls import patterns, include, url

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

    url(r'^(?P<id>\d+)/group/$', 'datapanel.views.group.home', name='group_home'),

    (r'^accounts/', include('registration.backends.default.urls')),
)
