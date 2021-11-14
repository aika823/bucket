from django.http import request
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Party, UserParty
from user.models import User
from .serializer import PartySerializer

def list(request):
    party_list = Party.objects.all()
    return render(request, 'party.html', {'party_list':party_list})

def create(request):
    return render(request, 'create.html', {'user_id': request.session.get("user")})

def detail(request, party_id):
    print("party detail ##################")
    party = Party.objects.get(id=party_id)
    return render(request, 'detail.html', {'party':party})



class PartyViewSet(viewsets.ViewSet):
    def create(self, request):

        print("##############################파티 생성 함수")

        print(request.POST)

        host = request.POST.get('host')
        host = User.objects.filter(id=host).all()[0]
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        address = request.POST.get('address')
        headcount = request.POST.get('headcount')
        price = request.POST.get('price')
        link = request.POST.get('link')
        

        party = Party(
            host=host,
            name=name,
            date=date,
            time=time,
            address=address,
            headcount=headcount,
            price=price,
            link=link
        )
        party.save()

        user_party = UserParty(
            user_id = party.host,
            party_id = party,
            is_host = True,
            is_join = True,
            is_like = True
        )
        user_party.save()
        
        queryset = Party.objects.all()
        serializer = PartySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def list():
        return "test"