import json
import requests
import base64

from os import access
from django.db.models.expressions import F, Case, When
from django.db.models.fields import CharField
from django.db.models.query_utils import Q, FilteredRelation

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.conf import settings
from requests.sessions import session
from user.social_login import callback

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from .models import Interest, User, UserInterest
from .forms import RegisterForm
from .serializer import InterestSerializer, UserInterestSerializer, UserSerializer
from .decorators import admin_required


billim_url = settings.BILLIM_URL
image_url = settings.IMAGE_URL

def profile(request):
    user_id =request.session.get('user') 
    user_list = User.objects.filter(id=user_id).values()
    if user_list:
        user = user_list[0]
        user_interest = UserInterest.objects.filter(user_id=user_id)
        return render(request, 'profile.html', {'user': user, 'user_interest':user_interest})
    else:
        return redirect('/user/login')

def index(request):
    return render(request, 'index.html', { 'email': request.session.get('user') })

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])
    return redirect('/')

def callback_social(request, type):    
    
    # Get user information from callback function
    user_info = callback(request,type)
    
    # DB에서 중복여부 확인 후 유저 정보 저장 
    try:
        user_in_db = User.objects.get(social_id=user_info['social_id'])
    except User.DoesNotExist:
        user_in_db = None
    if user_in_db:
        user = user_in_db
    else:
        user = User(
                    name=user_info['name'],
                    email=user_info['email'],
                    password=None,
                    social_login=type,
                    social_id = user_info['social_id']
                )
        user.save()

    # 소셜 로그인 후 홈페이지로 이동
    request.session['user'] = user.id
    return redirect('/user/profile')

def login(request):
    # 로그인 폼 제출 시
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            name = User.objects.filter(id=form.user_id).values('name')[0]['name']
            image_src = str(User.objects.filter(id=form.user_id).values('image')[0]['image'])
            return render(request, 'home.html', {'name':name, 'image_src':image_src})
    else:
        # 로그인 된 경우
        if 'user' in request.session: 
            user = User.objects.get(id=request.session['user'])
            form = None
        # 로그인 안 된 경우
        else: 
            user = None
            form = LoginForm()
        
    return render(request, 'login.html', {
        'form': form, 
        'user':user, 
    })

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')
        return super().form_valid(form)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class InterestViewSet(viewsets.ViewSet):
    def create(self, request):
        user_id =request.session.get('user') 
        user = User.objects.filter(id=user_id).all()[0] 
        interest = request.POST['interest']
        current_interests= Interest.objects.filter(interest=interest).all()
        if current_interests:
            interest = current_interests[0]
        else:
            interest = Interest(interest=interest)
            interest.save()
        current_user_interest = UserInterest.objects.filter(user_id=user_id ,interest_id=interest.id).all()
        if current_user_interest:
            pass
        else:
            user_interest = UserInterest(user_id=user, interest_id = interest)
            user_interest.save()
        queryset = Interest.objects.all()
        serializer = InterestSerializer(queryset, many=True)
        return Response(serializer.data)
    def list():
        return "test"

class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer