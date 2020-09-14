from django.shortcuts import render, get_object_or_404
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from users.models import Encrypt
from django.core.cache import cache
import pyaes
from base64 import b64encode,b64decode
# Create your views here.

"""
@login_required(login_url='/login')
def home(request, username=''):
    if username != request.user.username:
        return HttpResponseRedirect(reverse('blog-home',args=(request.user.username,)))
    context = {
        'posts': request.user.post.objects.order_by('-last_mod'),
        'user': username
    }
    return render(request, 'blogapp/home.html', context)
"""


class PostListView(LoginRequiredMixin,ListView):
    template_name = 'blogapp/home.html'
    model=Post
    context_object_name = 'posts'
    ordering = ['-last_mod']
    paginate_by = 1

    def get_queryset(self):
        self.check1()
        queryset=super(PostListView, self).get_queryset()
        queryset=queryset.filter(user=self.request.user)
        for q in queryset:
            content=b64decode(q.content.encode())
            enc = Encrypt.objects.get(user=self.request.user)
            aes = pyaes.AESModeOfOperationCBC(key=cache.get('dek_key'), iv=enc.iv_dek)
            decrypter=pyaes.Decrypter(aes)
            str1=decrypter.feed(content)
            str1+=decrypter.feed()
            q.content=str1.decode()
        return queryset

    def check1(self):
        if self.kwargs['username'] != self.request.user.username:
            return HttpResponseRedirect(reverse('blog-home', args=self.request.user.username))


class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post

    def get_object(self, queryset=None):
        cs=Post.objects.get(pk=self.kwargs['pk'])
        content=b64decode(cs.content.encode())
        enc=Encrypt.objects.get(user=self.request.user)
        aes=pyaes.AESModeOfOperationCBC(key=cache.get('dek_key'),iv=enc.iv_dek)
        decrypter=pyaes.Decrypter(aes)
        str1=decrypter.feed(content)
        str1+=decrypter.feed()
        cs.content=str1.decode()
        return cs


class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.user=self.request.user
        content=form.instance.content
        enc=Encrypt.objects.get(user=self.request.user)
        aes=pyaes.AESModeOfOperationCBC(key=cache.get('dek_key'),iv=enc.iv_dek)
        encryptor=pyaes.Encrypter(aes)
        str1 = encryptor.feed(content)
        str1 += encryptor.feed()
        str1=b64encode(str1)
        form.instance.content = str1.decode()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UpdateView):
    model=Post
    fields = ['title','content']

    def get_object(self, queryset=None):
        cs=Post.objects.get(pk=self.kwargs['pk'])
        content=b64decode(cs.content.encode())
        enc=Encrypt.objects.get(user=self.request.user)
        aes=pyaes.AESModeOfOperationCBC(key=cache.get('dek_key'),iv=enc.iv_dek)
        decrypter=pyaes.Decrypter(aes)
        str1=decrypter.feed(content)
        str1+=decrypter.feed()
        cs.content=str1.decode()
        return cs

    def form_valid(self, form):
        form.instance.user=self.request.user
        content = form.instance.content
        enc = Encrypt.objects.get(user=self.request.user)
        aes = pyaes.AESModeOfOperationCBC(key=cache.get('dek_key'), iv=enc.iv_dek)
        encryptor = pyaes.Encrypter(aes)
        str1 = encryptor.feed(content)
        str1 += encryptor.feed()
        str1 = b64encode(str1)
        form.instance.content = str1.decode()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('blog-home',args=(self.request.user.username,))


def about(request):
    print('about reached')
    return render(request,'blogapp/about.html',{'title':'about'})