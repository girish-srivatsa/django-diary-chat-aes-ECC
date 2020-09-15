from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MessageForm(forms.Form):
    content=forms.CharField(max_length=1000,label='')
    content.widget.attrs.update({'onChange':'change(this,writing)'})

    class Meta:
        fields=['content']