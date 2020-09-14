from django.db.models.signals import post_save,post_init
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .views import PostListView


