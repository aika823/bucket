from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

from user import social_login
from . import views

urlpatterns = [
    path('', views.list),
    path('create', views.create),
    path('detail/<int:party_id>', views.detail),
]