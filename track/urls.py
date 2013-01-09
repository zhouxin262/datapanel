from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       # url(r'^(?P<id>\d+)/groupby_value/$', 'track.views.groupby.value', name='track_groupby_value'),
                       url(r'^(?P<id>\d+)/groupby_action/$', 'track.views.groupby.action', name='track_groupby_action'),
                       url(r'^(?P<id>\d+)/get_url_by_value/$', 'track.views.get_url_by_value', name='track_get_url_by_value'),
                       url(r'^(?P<id>\d+)/get_referrer_url/$', 'track.views.get_referrer_url', name='track_get_referrer_url'),
                       )
