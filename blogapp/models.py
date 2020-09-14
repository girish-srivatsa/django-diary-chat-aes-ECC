import uuid

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    key=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=50)
    content=models.TextField(max_length=5000)
    last_mod=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title+" : "+self.content+" by "+self.user.username

    def get_absolute_url(self):
        return reverse('post-detail',args=(self.user.username,self.key))
