from django.http import request
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from user.models import User
import json
import datetime
from django.db.models import Count
from party.models import Comment, Party, UserParty

def main(request):
    count = dict()
    count['party'] = Party.objects.all().count()
    count['user'] = User.objects.all().count()
    count['comment'] = Comment.objects.all().count()
    return render(request, "manager_main.html", {'count':count})

def delete(request):
    if request.method == "POST":
        if request.POST.get('table') == 'party':
            party = Party.objects.get(id=request.POST.get('id'))
            party.delete()
            return redirect("manager:party")
        if request.POST.get('table') == 'user':
            user = User.objects.get(id=request.POST.get('id'))
            user.delete()
            return redirect("manager:user")
        if request.POST.get('table') == 'comment':
            comment = Comment.objects.get(id=request.POST.get('id'))
            comment.delete()
            return redirect("manager:comment")

def user(request):
    user_list = User.objects.all()
    return render(request, "manager_user.html", {'user_list':user_list})

def party(request):
    print("party")
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
    return render(request, "manager_party.html", {"party_list": party_list})

def comment(request):
    comment_list = Comment.objects.all()

    return render(request, "manager_comment.html", {"comment_list": comment_list})
