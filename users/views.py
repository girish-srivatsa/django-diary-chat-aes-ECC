import os
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from .forms import UserRegisterForm,LoginForm,UserUpdateForm
from .models import Profile
import cv2
import face_recognition
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog.settings import MEDIA_ROOT
from .models import Encrypt,ChatEncrypt
from os import urandom
import pyaes
from base64 import b64decode,b64encode
import hashlib
from django.core.cache import cache
from django.utils.encoding import force_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
from tinyec import registry
import secrets


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            passwd = form.cleaned_data.get('password1')
            form.save()
            usr = authenticate(request, username=username, password=passwd)
            if usr is not None:
                login(request,usr)
                enc = Encrypt.objects.create(user=usr)
                curve = registry.get_curve('secp256r1')
                enc_chat = ChatEncrypt.objects.create(user=usr)
                kek_chat = hashlib.pbkdf2_hmac('sha256', force_bytes(passwd), enc_chat.salt_kek, 1000)
                private_key = secrets.randbelow(curve.field.n)
                public=private_key*curve.g
                print(public.x)
                enc_chat.public_x = str(public.x)
                enc_chat.public_y = str(public.y)
                cache.add('private_key', private_key, version=1)
                cache.set('private_key', private_key, version=1)
                dek = urandom(32)
                cache.add('dek_key', dek, version=1)
                cache.set('dek_key', dek, version=1)
                kek = hashlib.pbkdf2_hmac('sha256', force_bytes(passwd), enc.salt_kek, 1000)
                aes = pyaes.AESModeOfOperationCBC(key=kek, iv=enc.iv_kek)
                encryptor = pyaes.Encrypter(aes)
                str1 = encryptor.feed(dek)
                str1 += encryptor.feed()
                enc.encrypted_dek = str1
                enc.save()
                aes = pyaes.AESModeOfOperationCBC(key=kek_chat, iv=enc_chat.iv_kek)
                encryptor = pyaes.Encrypter(aes)
                str1=encryptor.feed(str(private_key))
                str1+=encryptor.feed()
                enc_chat.encrypted_private = str1
                enc_chat.save()
            messages.success(request,f'Account Created for {username}')
            return HttpResponseRedirect(reverse('blog-home',args=(username,)))
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def known_encode():
    loaded_img=[]
    username=[]
    for i in Profile.objects.all():
        img_orig = face_recognition.load_image_file(i.image)
        img_locations = face_recognition.face_locations(img_orig)
        img_encode = face_recognition.face_encodings(img_orig, img_locations)[0]
        loaded_img.append(img_encode)
        username.append(i.user.username)
    return loaded_img,username


def login_view(request,redirect_field_name=REDIRECT_FIELD_NAME):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            img_encode, usernames = known_encode()
            cap = cv2.VideoCapture(0)
            _, cv2_im = cap.read()
            cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            cv2_locations = face_recognition.face_locations(cv2_im)
            cv2_encode = face_recognition.face_encodings(cv2_im, cv2_locations)[0]
            result = face_recognition.compare_faces(img_encode, cv2_encode)
            if True in result:
                first_match_index = result.index(True)
                username = usernames[first_match_index]
                passwd = form.cleaned_data.get('password')
                usr = User.objects.get(username=username)
                w1=passwd.encode()
                if usr.check_password(passwd):
                    login(request,usr)
                    enc=Encrypt.objects.get(user=usr)
                    enc_chat=ChatEncrypt.objects.get(user=usr)
                    encrypted_dek=enc.encrypted_dek
                    salt_kek=enc.salt_kek
                    kek = hashlib.pbkdf2_hmac('sha256', w1, salt_kek, 1000)
                    kek_chat=hashlib.pbkdf2_hmac('sha256',passwd.encode(),enc_chat.salt_kek,1000)
                    aes = pyaes.AESModeOfOperationCBC(key=kek, iv=enc.iv_kek)
                    decrypter=pyaes.Decrypter(aes)
                    dek = decrypter.feed(encrypted_dek)
                    dek += decrypter.feed()
                    aes = pyaes.AESModeOfOperationCBC(key=kek_chat, iv=enc_chat.iv_kek)
                    decrypter = pyaes.Decrypter(aes)
                    private = decrypter.feed(enc_chat.encrypted_private)
                    private += decrypter.feed()
                    private=int(private.decode())
                    cache.add('private_key',private,timeout=None)
                    cache.set('private_key', private,timeout=None)
                    cache.add('dek_key',dek,timeout=None,version=1)
                    cache.set('dek_key',dek,timeout=None,version=1)
                    messages.success(request, f'successful login {username}')
                    if redirect_to is not '':
                        return HttpResponseRedirect(redirect_to)
                    else:
                        return HttpResponseRedirect(reverse('blog-home',args=(username,)))
                else:
                    messages.warning(request,'wrong password')
            else:
                messages.warning(request, 'wrong username or person')

    else:
        form=LoginForm()
    return render(request,'users/login.html',{'form': form})


def logout_view(request):
    logout(request)
    cache.clear()
    return render(request,'users/logout.html')


@login_required(login_url='/login')
def profile(request,username):
    if username != request.user.username:
        return HttpResponseRedirect(reverse('profile',args=(request.user.username,)))
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            z=f'/media/profile_pic/{request.user.username}.jpeg'
            print(os.path.join(MEDIA_ROOT,z))
            u_form.save()
            if os.path.isfile(os.path.join(MEDIA_ROOT,z)):
                os.remove(os.path.join(MEDIA_ROOT,z))
            request.user.save()
            messages.success(request, f'successful update to {username}')
            return HttpResponseRedirect(reverse('profile', args=(request.user.username,)))
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request,'users/profile.html',{'u_form': u_form})