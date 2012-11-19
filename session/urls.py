from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<id>\d+)/stream/list/$', 'session.views.stream.list', name='stream_list'),
                       url(r'^(?P<id>\d+)/stream/$', 'session.views.stream.tile', name='stream_tile'),
                       url(r'^(?P<id>\d+)/stream/(?P<sid>\d+)/$', 'session.views.stream.view', name='stream_view'),

                       url(r'^(?P<id>\d+)/get_stream_by_value/$', 'session.views.stream.get_stream_by_value', name='stream_get_stream_by_value'),
                       # url(r'^(?P<id>\d+)/funnel/$', 'session.views.stream.funnel', name='stream_funnel'),
                       )



