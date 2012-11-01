from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^funnel/(?P<id>\d+)/$', 'funnel.views.home', name='funnel_home'),
                       url(r'^funnel/(?P<id>\d+)/list/$', 'funnel.views.list', name='funnel_list'),
                       url(r'^funnel/(?P<id>\d+)/create/$', 'funnel.views.create', name='funnel_create'),
                       url(r'^funnel/(?P<id>\d+)/(?P<funnel_id>\d+)/update/$', 'funnel.views.update', name='funnel_update'),
                       url(r'^funnel/(?P<id>\d+)/(?P<funnel_id>\d+)/delete/$', 'funnel.views.delete', name='funnel_delete'),

                       url(r'^funnel/(?P<id>\d+)/(?P<funnel_id>\d+)/action/$', 'funnel.views.action.list', name='funnel_actionlist'),
                       url(r'^funnel/(?P<id>\d+)/(?P<funnel_id>\d+)/action/create/$', 'funnel.views.action.create', name='funnel_actioncreate'),
                       url(r'^funnel/(?P<id>\d+)/(?P<funnel_id>\d+)/action/(?P<action_id>\d+)/update/$', 'funnel.views.action.update', name='funnel_actionupdate'),
                       url(r'^funnel/(?P<id>\d+)/(?P<funnel_id>\d+)/action/(?P<action_id>\d+)/delete/$', 'funnel.views.action.delete', name='funnel_actiondelete'),
                       )
