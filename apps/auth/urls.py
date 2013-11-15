from django.contrib.auth.views import login, logout
from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'login/',login,kwargs = {'template_name' : 'auth/login.html'}, name = 'grabhalo_login'),
	url(r'logout/', logout,kwargs = {'template_name' : 'auth/logout.html'}, name = 'grabhalo_logout'),
	url(r'register/','apps.auth.views.register', name = 'grabhalo_register'),
)