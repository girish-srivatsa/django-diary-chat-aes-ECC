from django.contrib import admin
from .models import ChatP2P,ChatMessage


admin.site.register(ChatMessage)
admin.site.register(ChatP2P)