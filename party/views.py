from django.http import request
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Party, UserParty
from user.models import User
from .serializer import PartySerializer


def list(request):
    party_list = Party.objects.all()
    for party in party_list:
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
    try:
        party.members = UserParty.objects.filter(party_id=party_id, is_host=False, is_join=True).all()
    except:
        party.members = None
    try:
        user.member = UserParty.objects.get(
            user_id=user, party_id=party_id
        )
    except:
        user.member = None
    return render(
        request, "detail.html", {"party": party, "user": user}
    )


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
