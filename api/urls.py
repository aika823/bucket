from django.conf.urls import url
from django.urls import path, include

from rest_framework import routers
from user.views import InterestViewSet, UserInterestViewSet
from party.views import PartyViewSet
from . import views

interest_view = InterestViewSet.as_view({
    'post':'create',
    'get':'list'
})

user_interest_view = UserInterestViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

party_view = PartyViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

urlpatterns = [
    path('user/login',views.login),
    

    path('interest/',interest_view),
    path('user_interest/',user_interest_view),
    
    path('party/', party_view)
]