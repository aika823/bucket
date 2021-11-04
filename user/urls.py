from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login),
    path('login/', views.login),    
    path('login/<str:type>/', views.login_social),
    path('callback/<str:type>/', views.callback_social),
    path('logout/', views.logout),
]