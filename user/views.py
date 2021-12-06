import json
import os
import re
from django.db import models
from django.db.models import query
from django.http.response import JsonResponse
import requests
import base64

from os import access, error
from django.db.models.expressions import F, Case, When
from django.db.models.fields import CharField
from django.db.models.query_utils import Q, FilteredRelation

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.conf import settings
from requests.sessions import session
from bucket.settings import BASE_DIR, PROJECT_ROOT, ROOT_DIR
from user.social_login import callback

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from party.models import UserParty

from .forms import RegisterForm
from .forms import LoginForm, RegisterForm
from .models import Interest, User, UserInterest
from .forms import RegisterForm
from .serializer import InterestSerializer, UserInterestSerializer, UserSerializer
from .decorators import admin_required
from django.contrib.auth.hashers import make_password

# views.py
# 기존에 사용하던 메소드
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib import auth


# 새로 추가하는 메소드
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template, render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from email.utils import formataddr

# from email.message import EmailMessage
import smtplib

from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

from email.utils import formataddr


class InterestViewSet(viewsets.ViewSet):
    def create(self, request):
        user_id = request.session.get("user")
        user = User.objects.filter(id=user_id).all()[0]
        interest = request.POST["interest"]
        current_interests = Interest.objects.filter(interest=interest).all()
        if current_interests:
            interest = current_interests[0]
        else:
            interest = Interest(interest=interest)
            interest.save()
        current_user_interest = UserInterest.objects.filter(
            user_id=user_id, interest_id=interest.id
        ).all()
        if current_user_interest:
            pass
        else:
            user_interest = UserInterest(user_id=user, interest_id=interest)
            user_interest.save()
        queryset = Interest.objects.all()
        serializer = InterestSerializer(queryset, many=True)
        # return Response(serializer.data)
        return redirect("user:profile")

    def list():
        return "test"


class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer


def delete(request):
    user_interest_id = request.GET.get("user_interest_id")
    user_interest = UserInterest.objects.get(id=user_interest_id)
    interest = user_interest.interest_id

    user_interest.delete()
    interest.delete()

    result = {"msg": "good"}
    return JsonResponse(result)


def update(request):
    if request.POST.get("user_id"):
        user_id = request.POST.get("user_id")
    else:
        user_id = request.session.get("user")
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        if request.FILES.get("image"):
            user.image = request.FILES.get("image")
        if request.POST.get("name"):
            user.name = request.POST.get("name")
        if request.POST.get("detail"):
            user.detail = request.POST.get("detail")
        if request.POST.get("instagram"):
            user.instagram = request.POST.get("instagram")
        if request.POST.get("password"):
            if request.POST.get("password") == request.POST.get("re_password"):
                user.password = make_password(request.POST.get("password"))
        user.save()
        return redirect("user:profile")


def profile(request):
    user_id = request.session.get("user")
    my = True
    if request.method == "GET":
        if request.GET.get("id"):
            user_id = request.GET.get("id")
            my = False
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("user:login")
    user_interest = (
        UserInterest.objects.filter(user_id=user_id).select_related("interest_id").all()
    )
    user_party = (
        UserParty.objects.filter(user_id=user_id).select_related("party_id").all()
    )
    return render(
        request,
        "profile.html",
        {
            "user": user,
            "user_interest": user_interest,
            "user_party": user_party,
            "my": my,
        },
    )


def index(request):
    if request.session.get("user"):
        return redirect("user:profile")
    else:
        return redirect("user:login")


def logout(request):
    if "user" in request.session:
        del request.session["user"]
    return redirect("user:login")


def callback_social(request, type):

    # Get user information from callback function
    user_info = callback(request, type)
    print(user_info)

    # DB에서 중복여부 확인 후 유저 정보 저장
    try:
        user_in_db = User.objects.get(social_id=user_info["social_id"])
    except User.DoesNotExist:
        user_in_db = None
    if user_in_db:
        user = user_in_db
    else:
        user = User(
            name=user_info["name"],
            email=user_info["email"],
            password=None,
            social_login=type,
            social_id=user_info["social_id"],
        )
        user.save()

    # 소셜 로그인 후 홈페이지로 이동
    request.session["user"] = user.id
    return redirect("user:profile")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session["user"] = user.id
                return redirect("user:profile")
            else:
                error = "비밀번호를 확인해주세요."
                return render(request, "login.html", {"error": error})
        except Exception as e:
            print(e)
            error = "존재하지 않는 회원입니다."
            return render(request, "login.html", {"error": error})
    else:
        try:
            user = User.objects.get(id=request.session.get("user"))
        except:
            user = None
        return render(request, "login.html", {"user": user})


def find_password(request):
    if request.method == "POST":
        user_email = request.POST.get("email")

        try:
            user = User.objects.get(email=user_email)
        except:
            return render(request, "find_password.html", {"error": "존재하지 않는 이메일입니다."})
        print(user)
        message = render_to_string(
            "find_password_email.html",
            {
                "user": user,
                "domain": get_current_site(request).domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                "token": account_activation_token.make_token(user),
            },
        )
        mail_subject = "[버킷리스터] 비밀번호 초기화 메일입니다."

        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()

        return redirect("user:find_password")
    else:
        return render(request, "find_password.html")


def register(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["re_password"]:
            user = User(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                password=make_password(request.POST.get("password")),
                is_active=False,
            )
            if request.FILES.get("image"):
                user.image = request.FILES.get("image")
            user.save()
            message = render_to_string(
                "activate_email.html",
                {
                    "user": user,
                    "domain": get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk))
                    .encode()
                    .decode(),
                    "token": account_activation_token.make_token(user),
                },
            )
            mail_subject = "[버킷리스터] 회원가입 인증 메일입니다."
            user_email = user.email
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return redirect("user:profile")
    else:
        return render(request, "register.html")


def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse("비정상적인 접근입니다.")

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        request.session["user"] = uid
        return redirect("user:profile")


def reset_password(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse("비정상적인 접근입니다.")

    if account_activation_token.check_token(user, token):
        request.session["user"] = uid
        return render(request, "reset_password.html", {"user": user})


import os
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_mail_test():

    rendered_report = RenderedReport.objects.get(pk=1)
    views = rendered_report.rendered_views.all()

    context = {"views": views}

    html_content = render_to_string("email.html", context=context).strip()

    subject = "HTML Email"
    to = ["aika823@naver.com"]
    reply_to = ["noreply@test.com"]

    msg = EmailMultiAlternatives(
        subject, html_content, "choiinkyu95@gmail.com", to, reply_to=reply_to
    )
    msg.content_subtype = "html"  # Main content is text/html
    msg.mixed_subtype = "related"  # This is critical, otherwise images will be displayed as attachments!

    for view in views:
        # Create an inline attachment
        image = MIMEImage(view.png.read())
        image.add_header("Content-ID", "<{}>".format(view.image_filename))
        msg.attach(image)
        
    msg.send()
