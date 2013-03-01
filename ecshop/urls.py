from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^(?P<id>\d+)/$', 'ecshop.views.overview', name='ecshop_overview'),
                       url(r'^(?P<id>\d+)/r2/$', 'ecshop.views.report2', name='ecshop_report2'),
                       url(r'^(?P<id>\d+)/orderinfo/$', 'ecshop.views.orderinfo', name='ecshop_orderinfo'),
                       )
