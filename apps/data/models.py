from django.db import models
from django.contrib.auth.models import  User

class GrabhaloUser(models.Model):
    name            = models.CharField(max_length = 64)
    phone           = models.IntegerField()
    GENDER          = (
                       ('m', 'Male'),
                       ('f', 'Female'),
                      )
    
    gender          = models.CharField(max_length=1, choices=GENDER, default='m')
    user            = models.ForeignKey(User)
    
    def __unicode__(self):
        return u"%s" % (self.name)


class WebQuery(models.Model):
    user_id         = models.IntegerField()
    conversation_id = models.IntegerField(default= 1)
    sent_to         = models.CharField(max_length = 500)
    user_query      = models.CharField(max_length = 500)
    date_time       = models.DateTimeField()


class WebReply(models.Model):
    conversation_id = models.IntegerField()
    user_id         = models.IntegerField()
    one_to_one_id   = models.IntegerField()
    sent_to         = models.IntegerField()
    chat            = models.CharField(max_length = 500)
    date_time       = models.DateTimeField()
