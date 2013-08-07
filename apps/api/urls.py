from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'get_data/','apps.api.views.get_data', name = 'grabhalo_get_data'),
)