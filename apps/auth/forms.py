from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.data.models import *

    
class GrabhaloRegister(UserCreationForm):
    name     = forms.CharField()
    phone    = forms.IntegerField() 
    gender   = forms.ChoiceField(choices=GrabhaloUser.GENDER)
    
    def save(self, *args, **kwargs):
        user = super(GrabhaloRegister,self).save(*args,**kwargs)
        
        GrabhaloUser.objects.create(user=user , gender=self.cleaned_data['gender'], 
        							name = self.cleaned_data['name'], 
        							phone = self.cleaned_data['phone'])
        
        return user

class ChatForm(forms.Form):
    chat    = forms.CharField(max_length=400, widget=forms.TextInput(attrs={'placeholder': 'Type Here!!!' }))

class UserForm(forms.Form):
    user    = forms.BooleanField()