import base64
from django.shortcuts import render, redirect
from django.conf import settings
import requests

project_url = settings.PROJECT_URL

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
        'naver' : settings.NAVER_CLIENT_ID,
        'kakao' : settings.KAKAO_CLIENT_ID,
        'google': settings.GOOGLE_CLIENT_ID
    }
    redirect_uri = {
        'naver' : project_url+'/user/callback/naver/',
        'kakao' : project_url+'/user/callback/kakao',
        'google': project_url+'/user/callback/google'
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
    if scope[type]: 
        str_auth += "&scope={}".format(scope[type])
    else:
        pass
    
    # callback 함수로 연결
    response = redirect(str_auth)
    return response 


def callback(request, type):    
    
    # 생성된 코드를 통해 유저 인증 진행
    code = request.GET.get('code')    
    url_auth = {
        'google': 'https://oauth2.googleapis.com/token',
        'naver' : 'https://nid.naver.com/oauth2.0/token',
        'kakao' : 'https://kauth.kakao.com/oauth/token'  
    }
    client_id={
        'naver' : settings.NAVER_CLIENT_ID,
        'kakao' : settings.KAKAO_CLIENT_ID,
        'google': settings.GOOGLE_CLIENT_ID
    }
    client_secret={
        'google': settings.GOOGLE_CLIENT_SECRET,
        'naver' : settings.NAVER_CLIENT_SECRET,
    }
    scope={
        'google': "https://www.googleapis.com/auth/userinfo.profile"
    }
    state={
        'naver' : "REWERWERTATE"
    }
    redirect_uri = {
        'google': project_url+'/user/callback/google',
        'naver' : project_url+'/user/callback/naver',
        'kakao' : project_url+'/user/callback/kakao'
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

    return user_info