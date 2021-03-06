from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from user import social_login
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.main, name='main'),
    path('user/', views.user, name='user'),
    path('party/', views.party, name='party'),
    path('comment/', views.comment, name='comment'),
    path('delete/', views.delete, name='delete')
]