from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from apps.auth.forms import *
from apps.data.models import *
from apps.dashboard.helpers import *
from itertools import chain
from operator import attrgetter
from django.db.models import Q
import re
from django.views.decorators.csrf import csrf_exempt
import json
import datetime


@login_required
@csrf_exempt
def dashboard(request):
	users = GrabhaloUser.objects.exclude(user_id = request.user.id)

	if request.is_ajax():
		if request.POST.has_key('message'):
			selected_users = request.POST.getlist('selected_users[]')
			message = request.POST['message']
			send_query(request,selected_users,message)
	
	ctx = { 'users' : users }

	return render_to_response('dashboard/dashboard.html',ctx, context_instance = RequestContext(request))


@csrf_exempt
@login_required
def chats(request):
	user_id = GrabhaloUser.objects.filter(user_id = request.user.id)[0].id
	chats = WebReply.objects.filter(sent_to = user_id)
	user_conversation_set = set()
	chats_dict = dict()

	if request.is_ajax():
		if request.POST.has_key('selected_message_id'):
			selected_message_id = (request.POST['selected_message_id']).split("_")
			user_id = selected_message_id[0]
			c_id = selected_message_id[1]
			web_reply = WebReply.objects.filter(conversation_id = c_id).filter( Q(user_id = user_id) |  Q(sent_to = user_id))

			for reply in web_reply:
				time = str(reply.date_time)
				message = reply.chat
				user_id = reply.user_id
				user_name = GrabhaloUser.objects.filter(id = user_id)[0].name
				chats_dict.update({time:{user_name:message}})
			print chats_dict
			return HttpResponse(json.dumps(chats_dict), content_type="application/json")

		elif request.POST.has_key("save_chat"):
			selected_chat_id = (request.POST['selected_chat_id']).split("_")
			sent_to = selected_chat_id[0]
			c_id = selected_chat_id[1]
			message = request.POST['message']
			date_time = datetime.datetime.now()
			web_reply = WebReply(sent_to = sent_to, conversation_id = c_id, chat = message, user_id = user_id, \
								date_time = date_time)
			web_reply.save()



	for chat in chats:
		user_conversation_set.add((chat.user_id,chat.conversation_id))

	message_list = dict()

	for user in user_conversation_set:
		user_conversation_id = str(user[0]) + "_" + str(user[1])
		message = WebReply.objects.filter(conversation_id = user[1], user_id = user[0])[0].chat
		user_name = GrabhaloUser.objects.filter(id = user[0])[0].name

		try: message_list[user_name].update({user_conversation_id:message})
		except : message_list.update({user_name:{user_conversation_id:message}})

	ctx = {"message_list" : message_list}
	return render_to_response('dashboard/chats.html',ctx, context_instance = RequestContext(request))