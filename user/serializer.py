from rest_framework import serializers
from .models import Interest, User, UserInterest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'social_login')

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'interest')

class UserInterestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    interest = InterestSerializer()
    # user = UserSerializer(read_only=True)
    # interest = InterestSerializer(read_only=True)
    class Meta:
        model = UserInterest
        fields = (
            'id',
            'user',
            'interest',
        )