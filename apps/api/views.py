from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
import datetime
from apps.data.models import *

def get_data(request):

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

	return HttpResponse(json.dumps(reply_dict), mimetype='application/json')