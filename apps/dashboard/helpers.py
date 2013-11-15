import datetime
from apps.data.models import *

def send_query(request,selected_users,query):

	date_time = datetime.datetime.now()
	web_query_data = WebQuery.objects.all()
	user_id = GrabhaloUser.objects.filter(user_id = request.user.id)[0].id
	if not web_query_data:
		c_id = 0
	else:
		for data in web_query_data:
			c_id = data.conversation_id


	web_query = WebQuery.objects.create(user_id = user_id, sent_to = selected_users, 
										user_query = query,date_time = date_time, conversation_id = c_id + 1)
	web_query.save()

	for user in selected_users : 
		
		web_reply = WebReply.objects.create(user_id = user_id, sent_to = user, chat = query, 
											conversation_id = c_id +1, date_time = date_time)
											
		web_reply.save()