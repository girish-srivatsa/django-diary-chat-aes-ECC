from django.urls import path,include
from . import views
from users import views as user_views
from blogapp import views as blog_views

urlpatterns = [
    path('',views.ChatListView.as_view(),name="chat-home"),
    path('create/',views.ChatCreateView.as_view(),name='chat-create'),
    path('<uuid:pk>/delete/',views.ChatDeleteView.as_view(),name='chat-delete'),
    path('<uuid:pk>/',views.chat_message_view,name='chat-view')
]