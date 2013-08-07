from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^dashboard/$','apps.dashboard.views.dashboard', name = 'grabhalo_dashboard'),
	url(r'^dashboard/chats/$','apps.dashboard.views.chats', name = 'grabhalo_chats'),
	)