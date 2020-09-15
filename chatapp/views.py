import hashlib
from base64 import b64encode, b64decode

import pyaes
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render,reverse
from django.views.generic.edit import FormMixin

from blogapp.models import Post
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from users.models import Encrypt, ChatEncrypt
from .models import ChatP2P,ChatMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MessageForm
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify, unhexlify
from tinyec import registry,ec
import secrets


class ChatListView(LoginRequiredMixin,ListView):
    template_name = 'chatapp/home.html'
    model = ChatP2P
    context_object_name = 'chats'
    ordering=['-last_msg_time']

    def get_queryset(self):
        queryset=super(ChatListView, self).get_queryset()
        queryset1=queryset.filter(user1=self.request.user)
        queryset2=queryset.filter(user2=self.request.user)
        queryset=queryset1 | queryset2
        return queryset


class ChatCreateView(LoginRequiredMixin,CreateView):
    model=ChatP2P
    fields = ['username2']
    success_url = ""

    def form_valid(self, form):
        user1=self.request.user
        if hasattr(user1, '_wrapped') and hasattr(user1, '_setup'):
            if user1._wrapped.__class__ == object:
                user1._setup()
            user1 = user1._wrapped
        username2=form.instance.username2
        user2=User.objects.get(username=username2)
        print(user1)
        print(user2)
        try:
            chat1_2=ChatP2P.objects.get(user1=user1,user2=user2)
        except ChatP2P.DoesNotExist:
            chat1_2 = None
        try:
            chat2_1 = ChatP2P.objects.get(user1=user2, user2=user1)
        except ChatP2P.DoesNotExist:
            chat2_1=None
        if user2 is None:
            print('no user2')
            return super().form_invalid(form)
        if user1 == user2:
            print('user1 == user2')
            return super(ChatCreateView, self).form_invalid(form)
        if chat1_2 is None:
            print('no chat exists 1,2')
            if chat2_1 is None:
                print('no chat exists 2,1')
                print(user1,user2)
                form.instance.user1 = user1
                form.instance.user2 = user2
                form.instance.username1 = user1.username
                form.instance.username2 = user2.username
                form.instance.creator = user1.username
                return super(ChatCreateView,self).form_valid(form)
            else:
                print('chat exists 2,1')
                print(user1, user2)
                return super().form_invalid(form)
        else:
            print('chat exists 1,2')
            return super().form_invalid(form)


class ChatDeleteView(LoginRequiredMixin,DeleteView):
    model = ChatP2P

    def get_success_url(self):
        return reverse('chat-home',args=(self.request.user.username,))


class ChatMessageListView(FormMixin,LoginRequiredMixin,ListView):
    template_name = 'chatapp/message.html'
    context_object_name = 'chatmessages'
    ordering = ['time']
    form_class = MessageForm

    def get_queryset(self):
        queryset = ChatMessage.objects.all()
        chatp2p=ChatP2P.objects.get(pk=self.kwargs['pk'])
        queryset.filter(chat=chatp2p)
        self.form=MessageForm(self.request.POST)
        if self.form.is_valid():
            content = self.form.cleaned_data.get('content')
            self.form = MessageForm()
            mess_from = self.request.user
            ChatMessage.objects.create(chat=chatp2p, mess_from=mess_from, message=content)
        return queryset


@login_required(login_url='login/')
def chat_message_view(request,username,pk):
    chatp2p = ChatP2P.objects.get(pk=pk)
    chats=ChatMessage.objects.filter(chat=chatp2p)
    enc=Encrypt.objects.get(user=request.user)
    other_user=request.user
    if chatp2p.user1 == request.user:
        other_user = chatp2p.user2
    else:
        other_user = chatp2p.user1
    chatp2p.save()
    enc_chat_other=ChatEncrypt.objects.get(user=other_user)
    curve = registry.get_curve('secp256r1')
    other_public_key_x=int(enc_chat_other.public_x)
    other_public_key_y = int(enc_chat_other.public_y)
    other_public_key=ec.Point(curve,other_public_key_x,other_public_key_y)
    my_private=cache.get('private_key')
    shared_key=my_private*other_public_key
    x_component = int.to_bytes(shared_key.x, 32, 'big')
    y_component = int.to_bytes(shared_key.y, 32, 'big')
    sha3_key = hashlib.sha3_256()
    sha3_key.update(x_component)
    sha3_key.update(y_component)
    secret_key = sha3_key.digest()
    for chat in chats:
        content=b64decode(chat.message1.encode())
        aes = pyaes.AESModeOfOperationCBC(key=secret_key, iv=chatp2p.iv)
        decrypter = pyaes.Decrypter(aes)
        str1=decrypter.feed(content)
        str1+=decrypter.feed()
        chat.message1=str1.decode()
    if request.method == 'POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data.get('content')
            mess_from=request.user
            enc_chat=ChatEncrypt.objects.get(user=other_user)
            aes = pyaes.AESModeOfOperationCBC(key=secret_key, iv=chatp2p.iv)
            encryptor = pyaes.Encrypter(aes)
            content=content.encode()
            str1=encryptor.feed(content)
            str1+=encryptor.feed()
            content=b64encode(str1).decode()
            ChatMessage.objects.create(chat=chatp2p,mess_from=mess_from,message1=content)
            if chatp2p.user1 == request.user:
                chatp2p.last_msg_1=chatp2p.last_msg
            else:
                chatp2p.last_msg_2=chatp2p.last_msg
            return HttpResponseRedirect(reverse('chat-view',args=(request.user.username,pk)))
    else:
        form=MessageForm()
    context={
        'chatmessages':chats,
        'form':form
    }
    return render(request,'chatapp/message.html',context)