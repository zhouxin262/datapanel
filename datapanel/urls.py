from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'datapanel.views.index', name='datapanel_index'),
    url(r'^track/$', 'datapanel.views.track', name='datapanel_track'),
    url(r'^(?P<id>\d+)/$', 'datapanel.views.home', name='datapanel_home'),
    url(r'^(?P<id>\d+)/delete/$', 'datapanel.views.delete', name='datapanel_delete'),
    url(r'^(?P<id>\d+)/setting/$', 'datapanel.views.setting', name='datapanel_setting'),
    url(r'^(?P<id>\d+)/stream/$', 'datapanel.views.stream', name='datapanel_stream'),
    url(r'^(?P<id>\d+)/stream/(?P<sid>\d+)/$', 'datapanel.views.stream_detail', name='datapanel_stream_detail'),
    url(r'^(?P<id>\d+)/group/$', 'datapanel.views.group', name='datapanel_group'),
    url(r'^create/$', 'datapanel.views.create', name='datapanel_create'),

    (r'^accounts/', include('registration.backends.default.urls')),
    # Examples:
    # url(r'^$', 'datapanel.views.home', name='home'),
    # url(r'^datapanel/', include('datapanel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
