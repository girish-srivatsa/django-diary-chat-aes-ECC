import uuid
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from os import urandom


class ChatP2P(models.Model):
    key = models.UUIDField(default=uuid.uuid4,primary_key=True)
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user1",null=True,blank=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user2",null=True,blank=True)
    username1=models.CharField(max_length=100,null=True,blank=True)
    username2 = models.CharField(max_length=100,null=True,blank=True)
    last_msg=models.CharField(blank=True,max_length=100)
    last_msg_time=models.DateTimeField(auto_now=True)
    last_msg_from=models.ForeignKey(User,on_delete=models.CASCADE,related_name="last_from",blank=True,null=True)
    creator=models.CharField(max_length=100,null=True,blank=True)
    iv=models.BinaryField(default=urandom(16))

    def __str__(self):
        return "user1:"+f'{self.user1}'+" user2:"+f'{self.user2}'

    def get_absolute_url(self):
        return reverse('chat-view',args=(self.creator,self.pk))


class ChatMessage(models.Model):
    chat = models.ForeignKey(ChatP2P,on_delete=models.CASCADE)
    mess_from = models.ForeignKey(User,on_delete=models.CASCADE)
    message1 = models.CharField(max_length=1000,null=True,blank=True)
    time = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)



