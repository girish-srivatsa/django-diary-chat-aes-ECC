from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import cv2
from PIL import Image
import io
import os
from blog.settings import MEDIA_ROOT


@receiver(post_save, sender=User)
def create_profile(sender, instance,created, **kwargs):
    if created:
        cap = cv2.VideoCapture(0)  # says we capture an image from a webcam
        _, cv2_im = cap.read()
        cap.release()
        cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        f = io.BytesIO()
        try:
            pil_im.save(f, format='jpeg')
            s = f.getvalue()
            image = ContentFile(s, f'{instance.username}.jpeg')
            Profile.objects.create(user=instance,image=image)
        finally:
            f.close()


@receiver(user_logged_in,sender=User)
def got_online(sender,user,request,**kwargs):
    user.profile.is_online=True
    user.profile.save()


@receiver(user_logged_out,sender=User)
def went_offline(sender,user,request,**kwargs):
    user.profile.is_online=False
    user.profile.save()


@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    instance.profile.save()


@receiver(post_save,sender=User)
def update_profile(sender,instance,created,**kwargs):
    cap = cv2.VideoCapture(0)  # says we capture an image from a webcam
    retval, cv2_im = cap.read()
    cap.release()
    if retval:
        cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        f = io.BytesIO()
        try:
            pil_im.save(f, format='jpeg')
            s = f.getvalue()
            tmp = instance.profile.image
            image = ContentFile(s, f'{instance.username}.jpeg')
            instance.profile.image=image
        finally:
            f.close()