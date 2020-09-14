from django.urls import path,include
from . import views
from users import views as user_views
from chatapp import views as chat_views

urlpatterns = [
    path('?username=<str:username>/', views.PostListView.as_view(),name="blog-home"),
    path('?username=<str:username>/post/<uuid:pk>/',views.PostDetailView.as_view(),name='post-detail'),
    path('?username=<str:username>/post/new/',views.PostCreateView.as_view(),name='post-create'),
    path('?username=<str:username>/post/<uuid:pk>/update/',views.PostUpdateView.as_view(),name='post-update'),
    path('?username=<str:username>/post/<uuid:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('?username=<str:username>/profile',user_views.profile,name='profile'),
    path('?username=<str:username>/chat/',include('chatapp.urls')),
    path('',user_views.register,name='register-redirect')
]
"""
path('<str:username>/<int:year1>/',views.year,name='blog-page')
"""