from django.conf.urls import url
from django.urls import path, include

from rest_framework import routers
import user


user_view = user.views.UserViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

interest_view = user.views.InterestViewSet.as_view({
    'post':'create',
    'get':'list'
})

user_interest_view = user.views.UserInterestViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

urlpatterns = [
    path('user/',user_view),
    path('interest/',interest_view),
    path('user_interest/',user_interest_view),
]