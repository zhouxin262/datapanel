from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url(r'^(?P<id>\d+)/$', 'ecshop.views.overview', name='ecshop_overview'),

)
