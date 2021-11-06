import json
from os import access
from django.db.models.expressions import F, Case, When
from django.db.models.fields import CharField
from django.db.models.query_utils import Q, FilteredRelation
import requests
import base64

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.conf import settings
from requests.sessions import session
from rest_framework import viewsets

from user.serializer import InterestSerializer, UserInterestSerializer, UserSerializer

from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from .models import Interest, User, UserInterest
from .forms import RegisterForm
from user.decorators import admin_required
from rest_framework.response import Response
from rest_framework.decorators import action



client_id_naver = settings.NAVER_CLIENT_ID
client_id_kakao = settings.KAKAO_CLIENT_ID
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

def login_social(request, type):
    url_auth = {
        'naver' : "https://nid.naver.com/oauth2.0/authorize",
        'kakao' : "https://kauth.kakao.com/oauth/authorize",
        'google': "https://accounts.google.com/o/oauth2/v2/auth"
    }
    response_type = {
        'naver' : 'code',
        'kakao' : 'code',
        'google': 'code'
    }
    client_id = {
        'naver' : 'WO73y3DTPypJ9B7qq56N',
        'kakao' : 'afa386bd37692148a6c914da561c8458',
        'google': '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com'
    }
    redirect_uri = {
        'naver' : billim_url+'/user/callback/naver/',
        'kakao' : billim_url+'/user/callback/kakao',
        'google': billim_url+'/user/callback/google'
    }
    scope={
        'naver' : None,
        'kakao' : None,
        'google': "https://www.googleapis.com/auth/userinfo.email "+"https://www.googleapis.com/auth/userinfo.profile"
    }
    state = {
        'naver' : '7a74649e-d714-438f-a3fc-991c8b6f4bc7',
        'kakao' : None,
        'google': None
    }
    str_auth = f"{url_auth[type]}?response_type={response_type[type]}&client_id={client_id[type]}&redirect_uri={redirect_uri[type]}&state={state[type]}"
    if scope[type]: str_auth += "&scope={}".format(scope[type])
    response = redirect(str_auth)
    return response
    
def callback_social(request, type):    
    
    # 생성된 코드를 통해 유저 인증 진행
    code = request.GET.get('code')    
    url_auth = {
        'google': 'https://oauth2.googleapis.com/token',
        'naver' : 'https://nid.naver.com/oauth2.0/token',
        'kakao' : 'https://kauth.kakao.com/oauth/token'  
    }
    client_id={
        'google': '1094555666329-b76moi8dkckmoe3vc9kb2qhf60r8t563.apps.googleusercontent.com',
        'naver' : "WO73y3DTPypJ9B7qq56N",
        'kakao' : '8697dec0f53599c5d7f2502389d16f72'
    }
    client_secret={
        'google': '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', #구글
        'naver' : "SOUKrwtgel", #네이버
    }
    scope={
        'google': "https://www.googleapis.com/auth/userinfo.profile"
    }
    state={
        'naver' : "REWERWERTATE"
    }
    redirect_uri = {
        'google': billim_url+'/user/callback/google',
        'naver' : billim_url+'/user/callback/naver',
        'kakao' : billim_url+'/user/callback/kakao',
    }
    if type == 'naver':
        clientConnect = client_id[type] + ":" + client_secret[type]
        clidst_base64 = base64.b64encode(bytes(clientConnect, "utf8")).decode()
        headers = {"Authorization": "Basic "+clidst_base64}
    else:
        headers = None
        
    data = {
        "grant_type":'authorization_code',
        'client_id':client_id[type],
        'redirect_uri':redirect_uri[type],
        'code':code,
    }
    if type in client_secret:
        data['client_secret'] = client_secret[type]
    if type in scope:
         data['scope'] = scope[type] 
    if type in state:
        data['state'] = state[type] 
    response = requests.request("POST", url_auth[type], data=data,headers=headers).json()
    
    # 액세스 토큰 발급
    access_token = response['access_token'] 

    # 액세스 토큰을 통해 유저 정보 요청
    if type == 'google':
        url_user_info = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_response = requests.request("POST", url_user_info, params={'access_token': access_token }).json()
        name = user_response['email']
        email = user_response['email']
        social_id = user_response['sub']

    elif type == 'naver':
        url_user_info = "https://openapi.naver.com/v1/nid/me"
        header = {'Authorization':"Bearer " + access_token}
        user_response = requests.request("POST", url_user_info, headers=header).json()
        name = user_response['response']['name']
        email = user_response['response']['email']
        social_id = user_response['response']['id']
    
    elif type == 'kakao':
        url_user_info = "https://kapi.kakao.com/v2/user/me"
        header = {'Authorization':"Bearer " + access_token}
        user_response = requests.request("POST", url_user_info, headers=header, verify=False).json()
        name = user_response['kakao_account']['profile']['nickname'] #카카오
        email = user_response['kakao_account']['email']
        social_id = user_response['id']

    # 유저 정보
    user_info = {
        'name': name,
        'email': email,
        'social_id': social_id
    }
    
    # DB에서 중복여부 확인 후 유저 정보 저장 
    try:
        user_in_db = User.objects.get(social_id=social_id)
    except User.DoesNotExist:
        user_in_db = None

    if user_in_db:
        user = user_in_db
    else:
        user = User(
                    name=name,
                    email=email,
                    password=None,
                    social_login=type,
                    social_id = social_id
                )
        user.save()

    # 소셜 로그인 후 홈페이지로 이동
    request.session['user'] = user.id

    
    # request.session['user_obj'] = user 
    # 이거 넣고싶은데 안되네...



    # return render(request, 'home.html', {'test': user_info})
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

# class InterestViewSet(viewsets.ModelViewSet):
#     queryset = Interest.objects.all()
#     serializer_class = InterestSerializer

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
'''  '''
class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer