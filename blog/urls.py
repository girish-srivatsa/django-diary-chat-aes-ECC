"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from blogapp import views as blog_views
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',blog_views.about,name='blog-about'),
    path('register/',users_views.register,name='register'),
    path('login/',users_views.login_view,name='login'),
    path('logout/',users_views.logout_view,name='logout'),
    path('',users_views.register,name='register'),
    path('',include('blogapp.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
