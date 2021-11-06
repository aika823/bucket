from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from user import social_login
from . import views

urlpatterns = [
    path('', views.login),
    path('profile', views.profile),
    path('login/', views.login),    
    path('login/<str:type>/', views.login_social),
    path('login/<str:type>/', social_login.login_social),
    path('callback/<str:type>/', views.callback_social),
    path('logout/', views.logout),
]