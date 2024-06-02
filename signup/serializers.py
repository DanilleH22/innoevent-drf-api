
from rest_framework import serializers
from .models import SignUp
from events.serializers import EventSerializer
from django.contrib.auth.models import User
from events.models import Events

# class UserRelatedProfileSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer(source='userprofile', read_only=True) 
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'profile']

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = SignUp
        fields = ['event', 'attendee', 'name', 'email']
        read_only_fields = ['attendee']  

    def create(self, validated_data):
        validated_data['attendee'] = self.context['request'].user
        return super().create(validated_data)