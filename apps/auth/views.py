from django.shortcuts import render_to_response,redirect,render
from django.conf.urls.defaults import *
from django.template import RequestContext
from django.contrib.auth import logout,login,authenticate
from apps.auth.forms import *
from apps.data.models import *
from django.conf import settings

def register(request):
	form = GrabhaloRegister(request.POST or None)
	
	if(form.is_valid()):
		user = form.save()
		user.backend = settings.AUTHENTICATION_BACKENDS[0]
		login(request,user)
		return redirect('/dashboard/')

	ctx = {
			'form' : form
	}

	return render_to_response('auth/register.html',ctx, context_instance = RequestContext(request))