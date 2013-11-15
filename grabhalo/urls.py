from django.conf.urls import patterns, include, url
from grabhalo import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^',include('apps.auth.urls')),
	url(r'^',include('apps.api.urls')),
	url(r'^dashboard/',include('apps.dashboard.urls')),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'grabhalo.views.home', name='home'),
    # url(r'^grabhalo/', include('grabhalo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)