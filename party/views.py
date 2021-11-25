from django.http import request
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .models import Comment, Party, UserParty, UserComment
from user.models import User
from .serializer import PartySerializer

import json
import datetime

from django.db.models import Count, Q
from django.template import loader


def search(request):
    return render(request, "search.html")
    
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    if(request.GET.get('date')):
        date = request.GET.get('date')[0] 
    else:
        date = None
    day_of_week = request.GET.getlist('day-of-week')
    category_list = request.GET.getlist('category')
    
    party_list = Party.objects.all()
    current_week = datetime.date.today().isocalendar()[1] 

    if(date == '이번주'):
        party_list = party_list.filter(date__week=current_week)
    if(date == '다음주'):
        party_list = party_list.filter(date__month=current_week+1)
    if(start and end):
        party_list = party_list.filter(date__range=[start, end])
    if(day_of_week):
        party_list = party_list.filter(date__week_day__in=day_of_week)
    if(category_list):
        party_list = party_list.filter(category__in=category_list)

    
    return render(request, "search.html", {'party_list':party_list})

def get_comment(request):
    comment_id = request.GET.get('comment_id')
    parent_comment = Comment.objects.get(id=comment_id)
    comment_list = Comment.objects.filter(parent=parent_comment)
    template = loader.get_template('comment.html')
    parent_comment.count_like = UserComment.objects.filter(comment=parent_comment, is_like=True).all().count()

    user = User.objects.get(id=request.session.get("user"))
    try:
        queryset = UserComment.objects.filter(user=user, is_like=True)
        result_list = []
        for object in queryset:
            result_list.append(object.comment.id)
        user.user_comment = result_list
    except:
        user.user_comment =  None

    context = {
        'comment_list': comment_list,
        'parent_comment': parent_comment,
        'user': user
    }  
    return HttpResponse(template.render(context,request))

def comment(request):
    if request.method == "POST":
        
        user = User.objects.get(id=request.session.get("user"))
        try:
            party = Party.objects.get(id=request.POST.get('party_id'))
        except:
            party = None
        try:
            parent = Comment.objects.get(id=request.POST.get('parent_id')) 
            party = parent.party
            print(party)
        except:
            parent = None

        content = request.POST.get('content')
        
        comment = Comment()
        comment.content = content
        comment.user = user
        comment.party = party
        comment.parent = parent
        comment.save()

    return redirect("/party/detail/" + str(party.id))


def like(request):
    user = User.objects.get(id=request.session.get("user"))
    
    if request.GET.get('id') and request.GET.get('table')=='party':
        party = Party.objects.get(id=request.GET.get('id'))
        try:
            relation = UserParty.objects.get(user_id=user, party_id=party)
        except:
            relation = UserParty()
            relation.user_id = user
            relation.party_id = party
            
    if request.GET.get('id') and request.GET.get('table')=='comment': 
        comment = Comment.objects.get(id=request.GET.get('id'))
        try:
            relation = UserComment.objects.get(user=user, comment=comment)
        except:
            relation = UserComment()
            relation.user = user
            relation.comment = comment

    if(request.GET.get('like')=='true'):
        relation.is_like = True
    else:
        relation.is_like = False

    relation.save()
    dict = {
        "message": "업데이트 성공",
    }
    return JsonResponse(dict)


def list(request):
    user = User.objects.get(id=request.session.get("user"))

    if(request.GET):

        print(request.GET)

        start = request.GET.get('start_date')
        end = request.GET.get('end_date')
        if(request.GET.get('date')):
            date = request.GET.get('date')
        else:
            date = None
        day_of_week = request.GET.getlist('day-of-week')
        category_list = request.GET.getlist('category')
        
        party_list = Party.objects.all()
        current_week = datetime.date.today().isocalendar()[1] 

        print("date")
        print(date)

        if(date == '이번주'):
            party_list = party_list.filter(date__week=current_week)
        if(date == '다음주'):
            party_list = party_list.filter(date__week=current_week+1)
        if(start and end):
            party_list = party_list.filter(date__range=[start, end])
        if(day_of_week):
            party_list = party_list.filter(date__week_day__in=day_of_week)
        if(category_list):
            party_list = party_list.filter(category__in=category_list)

        print(party_list.query)
    
    else:    
        party_list = Party.objects.all()
    
    # party_list = Party.objects.all()
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
        comments = Comment.objects.filter(party_id=party_id).all()
        for comment in comments:
            comment.count_like = UserComment.objects.filter(comment=comment, is_like=True).all().count()
            comment.count_children = Comment.objects.filter(parent=comment).all().count()
        party.comments = comments
    except:
        party.comments = None
    try:
        user.member = UserParty.objects.get(user_id=user, party_id=party_id)
    except:
        user.member = None
    try:
        queryset = UserComment.objects.filter(user=user, is_like=True)
        result_list = []
        for object in queryset:
            result_list.append(object.comment.id)
        user.user_comment = result_list
    except:
        user.user_comment =  None

    
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
            user_party.save()
            return redirect("/party/detail/" + str(party.id))
        else:
            user_party.is_join = True
            user_party.save()
            return HttpResponse (json.dumps({ 'data': 'good' }))
    else:
        return redirect("/party/")


class PartyViewSet(viewsets.ViewSet):
    def create(self, request):
        host = request.POST.get("host")
        host = User.objects.filter(id=host).all()[0]
        name = request.POST.get("name")
        category = request.POST.get("category")
        date = request.POST.get("date")
        time = request.POST.get("time")
        address = request.POST.get("address")
        headcount = request.POST.get("headcount")
        price = request.POST.get("price")
        link = request.POST.get("link")
        party = Party(
            host=host,
            name=name,
            category = category,
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
        return redirect("party:list")
        return Response(serializer.data)
        

    def list():
        return "test"
