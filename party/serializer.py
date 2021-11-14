from rest_framework import serializers
from .models import Party, UserParty
from user.serializer import UserSerializer

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('id', 'link')

class UserPartySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    party = PartySerializer()
    class Meta:
        model = UserParty
        fields = (
            'id'
        )