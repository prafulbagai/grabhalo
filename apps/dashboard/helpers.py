from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
import datetime
from apps.data.models import *

def send_query(request,selected_users,query):

	date_time = datetime.datetime.now()
	web_query_data = WebQuery.objects.all()
		
	if not web_query_data:
		c_id = 0
	else:
		for data in web_query_data:
			c_id = data.conversation_id


	web_query = WebQuery.objects.create(user_id = request.user.id, sent_to = selected_users, 
										user_query = query,date_time = date_time, conversation_id = c_id + 1)
	web_query.save()

	for user in selected_users : 
		web_reply_data = WebReply.objects.all()

		if not web_reply_data:
			one_to_one_id = 0
		else:
			for data in web_reply_data:
				one_to_one_id = data.one_to_one_id

		web_reply = WebReply.objects.create(user_id = request.user.id, sent_to = user, chat = query, 
											conversation_id = c_id +1, date_time = date_time,
											one_to_one_id = one_to_one_id + 1)
		web_reply.save()



def send_reply(request,conversation_id,selected_users,reply):
	
	date_time = datetime.datetime.now()
	
	for user in selected_users : 
		web_reply_data = WebReply.objects.all()

		if not web_reply_data:
			one_to_one_id = 0
		else:
			for data in web_reply_data:
				one_to_one_id = data.one_to_one_id

		web_reply = WebReply.objects.create(user_id = request.user.id, sent_to = user, chat = reply, 
											conversation_id = conversation_id, date_time = date_time,
											one_to_one_id = one_to_one_id + 1)
		web_reply.save()