from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from user import social_login
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index),
    path('profile', views.profile, name='profile'),
    path('login/', views.login, name='login'),    
    path('login/<str:type>/', social_login.login_social),
    path('callback/<str:type>/', views.callback_social),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    # path('activate', views.activate),
    path('activate/<uidb64>/<token>/', views.activate,  name='activate')

]