from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<id>\d+)/(?P<referrer_attr>site|keyword)/$', 'referrer.views.session',
                           name='session_groupby_referrer'),
                       url(r'^(?P<id>\d+)/order/keyword/$', 'referrer.views.order_keyword', name='session_order_keyword'),
                       )
