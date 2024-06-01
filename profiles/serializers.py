from rest_framework import serializers
from .models import Profile
from signup.models import SignUp
from events.serializers import EventSerializer

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    signed_up = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_signed_up(self, obj):
        signups = SignUp.objects.filter(attendee=obj.owner)
        events = [signup.event for signup in signups]
        return EventSerializer(events, many=True, context=self.context).data

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'biography', 'is_owner',
            'signed_up'
        ]