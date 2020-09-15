from django.db.models.signals import post_save,post_init
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ChatMessage,ChatP2P


@receiver(post_init,sender=ChatMessage)
def create_message(sender,instance,**kwargs):
    chatp2p = instance.chat
    key = instance.key
    user1 = chatp2p.user1
    user2 = chatp2p.user2
    chatp2p.last_msg = key
    if instance.mess_from == user1:
        chatp2p.last_msg_1 = key
    else:
        chatp2p.last_msg_2 = key
    chatp2p.save()