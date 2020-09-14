from django.db import models
from django.contrib.auth.models import User
from os import urandom


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='image_profile/girish.jpeg',upload_to='profile_pic')
    is_online=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class Encrypt(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    salt_kek=models.BinaryField(default=urandom(8))
    iv_kek=models.BinaryField(default=urandom(16))
    iv_dek=models.BinaryField(default=urandom(16))
    encrypted_dek=models.BinaryField(blank=True,null=True)

    def __str__(self):
        return f'{self.user.username}'


class ChatEncrypt(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    salt_kek=models.BinaryField(default=urandom(8))
    iv_kek=models.BinaryField(default=urandom(16))
    encrypted_private=models.BinaryField(blank=True,null=True)
    public_x=models.CharField(max_length=1000,blank=True,null=True)
    public_y = models.CharField(max_length=1000,blank=True, null=True)