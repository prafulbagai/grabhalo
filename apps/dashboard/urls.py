from django.conf.urls import patterns, url

urlpatterns = patterns('apps.dashboard.views',
	url(r'^$','dashboard', name = 'grabhalo_dashboard'),
	url(r'chats/$','chats', name = 'grabhalo_chats'),
	)