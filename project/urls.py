from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^create/$', 'project.views.create', name='project_create'),
   url(r'^(?P<id>\d+)/$', 'project.views.home', name='project_home'),
   url(r'^(?P<id>\d+)/overview/$', 'project.views.overview', name='project_overview'),
   url(r'^(?P<id>\d+)/monitor/$', 'project.views.monitor', name='project_monitor'),
   url(r'^(?P<id>\d+)/delete/$', 'project.views.delete', name='project_delete'),
   url(r'^(?P<id>\d+)/setting/$', 'project.views.setting', name='project_setting'),


   url(r'^(?P<id>\d+)/action/$', 'project.views.action.list', name='action_list'),
   url(r'^(?P<id>\d+)/action/create/$', 'project.views.action.create', name='action_create'),
   url(r'^(?P<id>\d+)/action/(?P<aid>\d+)/update/$', 'project.views.action.update', name='action_update'),
   url(r'^(?P<id>\d+)/action/(?P<aid>\d+)/delete/$', 'project.views.action.delete', name='action_delete'),

)
