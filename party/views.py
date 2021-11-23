from django.http import request
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .models import Comment, Party, UserParty
from user.models import User
from .serializer import PartySerializer

import json
import datetime

from django.db.models import Count


def comment(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session.get("user"))
        party = Party.objects.get(id=request.POST.get('party_id'))
        content = request.POST.get('content')

        comment = Comment()
        comment.content = content
        comment.user = user
        comment.party = party
        comment.save()

    return redirect("/party/detail/" + str(party.id))


def like(request):
    party = Party.objects.get(id=request.POST.get('party_id'))
    user = User.objects.get(id=request.session.get("user"))
    user_party = UserParty.objects.get(user_id=user, party_id=party)
    if(request.POST.get('like')=='true'):
        user_party.is_like = True
    else:
        user_party.is_like = False
    user_party.save()
    dict = {
        "message": "안녕 파이썬 장고",
    }
    return JsonResponse(dict)


def list(request):
    user = User.objects.get(id=request.session.get("user"))
    party_list = Party.objects.all()
    for party in party_list:
        party.d_day = (party.date - datetime.date.today()).days
        
        try:
            party.like_count = UserParty.objects.filter(party_id=party, is_like=True).annotate(like_count=Count('is_like')).count()
        except:
            party.like_count = 0


        try:
            UserParty.objects.get(party_id=party, user_id=user, is_like=True)
            party.user_like = True
        except:
            party.user_like = False
        
        try:
            party.members = UserParty.objects.filter(party_id=party.id, is_join=True)
        except:
            party.members = None


    return render(request, "party.html", {"party_list": party_list})


def create(request):
    return render(request, "create.html", {"user_id": request.session.get("user")})


def detail(request, party_id):
    user = User.objects.get(id=request.session.get("user"))
    party = Party.objects.get(id=party_id)
    party.d_day = (datetime.date.today() - party.date).days
    try:
        party.members = UserParty.objects.filter(
            party_id=party_id, is_host=False, is_join=True
        ).all()
        party.leftover = party.headcount - len(party.members)
    except:
        party.members = None
    
    try:
        party.comments = Comment.objects.filter(party_id=party_id).all()
    except:
        party.comments = None
    try:
        user.member = UserParty.objects.get(user_id=user, party_id=party_id)
    except:
        user.member = None
    
    return render(request, "detail.html", {"party": party, "user": user})


def join(request):

    if request.method == "POST":
        user = User.objects.get(id=request.session.get("user"))
        party = Party.objects.get(id=request.POST.get("party_id"))

        try:
            user_party = UserParty.objects.get(user_id=user, party_id=party)
        except:
            user_party = UserParty()
            user_party.user_id = user
            user_party.party_id = party

        print(user_party)

        if user_party.is_join:
            user_party.is_join = False
        else:
            user_party.is_join = True

        user_party.save()
        return redirect("/party/detail/" + str(party.id))
    else:
        return redirect("/party/")


class PartyViewSet(viewsets.ViewSet):
    def create(self, request):
        host = request.POST.get("host")
        host = User.objects.filter(id=host).all()[0]
        name = request.POST.get("name")
        date = request.POST.get("date")
        time = request.POST.get("time")
        address = request.POST.get("address")
        headcount = request.POST.get("headcount")
        price = request.POST.get("price")
        link = request.POST.get("link")
        party = Party(
            host=host,
            name=name,
            date=date,
            time=time,
            address=address,
            headcount=headcount,
            price=price,
            link=link,
        )
        party.save()

        user_party = UserParty(
            user_id=party.host, party_id=party, is_host=True, is_join=True, is_like=True
        )
        user_party.save()

        queryset = Party.objects.all()
        serializer = PartySerializer(queryset, many=True)
        return Response(serializer.data)

    def list():
        return "test"
