from rest_framework import serializers
from .models import Interest, User, UserInterest

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = '__all__'

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