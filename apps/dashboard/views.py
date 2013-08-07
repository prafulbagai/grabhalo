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

@login_required
def dashboard(request):
	users = GrabhaloUser.objects.all()
	form = ChatForm(request.POST or None)
	#check_form = UserForm(request.POST or None)

	if request.method == 'POST':
		if(form.is_valid()):# and check_form.is_valid()):
			selected_users = request.POST.getlist('users')
			#selected_users = check_form.cleaned_data['user']
			query = form.cleaned_data['chat']
			send_query(request,selected_users,query)

	ctx = {
			'users' : users,
			'form'	: form,
	#		'check_form' : check_form,
	}

	return render_to_response('dashboard/dashboard.html',ctx, context_instance = RequestContext(request))
	
@login_required
def chats(request):

	#----------SEND REPLY-------------
	form = ChatForm(request.POST or None)

	if request.method == 'POST':
		if(form.is_valid()):
			
			reply_id =  map(int, re.findall(r'\d+', str(request.POST.getlist('reply_id'))))
			conversation_id = reply_id[0]
			reply_id.pop(0)
			selected_users = reply_id
			reply = form.cleaned_data['chat']
			send_reply(request,conversation_id,selected_users,reply)

	#--------END OF SEND REPLY--------

	#--------GET CHAT DATA------------
	DATE_FORMAT = "%Y-%m-%d" 
	TIME_FORMAT = "%H:%M:%S"
	
	chat_dict = {}

	web_reply_data = WebReply.objects.filter( Q(user_id = request.user.id) |  Q(sent_to = request.user.id))

	web_query_data = WebQuery.objects.filter(user_id = request.user.id).order_by('-date_time')

	chat_data = sorted(chain(web_reply_data,web_query_data), key=attrgetter('date_time'),reverse = True)
	
	#for data in chat_data:

	for data in web_query_data:
		conversation_id = data.conversation_id
		sent_to_ids = set(data.sent_to)
		sent_to_name_list = list()
	
		for ids in sent_to_ids:

			if ids.isdigit():
				
				user_name = GrabhaloUser.objects.filter(user_id =  ids)

				for name in user_name: 
					sent_to_name = name.name

				web_reply_data = WebReply.objects.filter(conversation_id = conversation_id).filter( Q(user_id = ids) |  Q(sent_to = ids))

				if web_reply_data.count() > 1:

					reply_dict={"chat":[]}		
					for chat in web_reply_data:
						send_by_name = GrabhaloUser.objects.filter(user_id =  chat.user_id)

						if send_by_name.count() == 0:
							send_by_name = "Admin"
						else:
							for name in send_by_name: 
								send_by_name = name.name						

						reply_dict["chat"].append({"reply" : chat.chat , "sent_to" : chat.sent_to,
												   "send_by" : send_by_name,
											       "date_time" : chat.date_time.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT)) })
					
					chat_dict.update({str(data.conversation_id) + '_' + str(ids) : { 
									 "sent_to_name" : sent_to_name,
									 "chat" : reply_dict["chat"] } } )
				else:
					send_by_name = GrabhaloUser.objects.filter(user_id =  data.user_id)

					if send_by_name.count() == 0:
						send_by_name = "Admin"
					else:
						for name in send_by_name: 
							send_by_name = name.name					
					
					sent_to_name_list.append(str(sent_to_name))
					reply_dict={"chat":[]}		
					reply_dict["chat"].append({"reply" : data.user_query , "sent_to" : sent_to_ids,
											   "send_by" : send_by_name,
											   "date_time" : data.date_time.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT)) })					
					chat_dict.update({str(data.conversation_id) + '_' + str(sent_to_ids) : { 
									 "sent_to_name" : sent_to_name_list,
									 "chat" : reply_dict["chat"] } } )
	
	ctx ={
			'chat_dict' : chat_dict,
			'form'		: form,
	}
	return render_to_response('dashboard/chats.html',ctx, context_instance = RequestContext(request))



