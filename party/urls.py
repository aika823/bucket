from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from user import social_login
from . import views

app_name = "party"

urlpatterns = [
    path('', views.list, name='list'),
    path('create', views.create),
    path('delete', views.delete),
    path('join', views.join),
    path('comment', views.comment),
    path('like', views.like),
    path('search', views.search),
    path('detail/<int:party_id>', views.detail, name='detail'),
    path('get_comment', views.get_comment, name='get_comment'),
]