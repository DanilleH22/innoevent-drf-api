
from rest_framework import serializers
from .models import SignUp
from events.serializers import EventSerializer
from django.contrib.auth.models import User
from events.models import Events


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = SignUp
        fields = ['event', 'attendee', 'name', 'email']
        read_only_fields = ['attendee']  

    def create(self, validated_data):
        validated_data['attendee'] = self.context['request'].user
        return super().create(validated_data)