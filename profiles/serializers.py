from rest_framework import serializers
from .models import Profile
from signup.models import SignUp
from events.models import Events
from events.serializers import EventSerializer

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    signed_up_events = serializers.SerializerMethodField()
    owned_events = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_signed_up_events(self, obj):
        sign_ups = SignUp.objects.filter(attendee=obj.owner)
        events = [sign_up.event for sign_up in sign_ups]
        serializer = EventSerializer(events, many=True, context=self.context)
        return serializer.data
    
    def get_owned_events(self, obj):
        owned_events = obj.owner.owned_events.all()
        return EventSerializer(owned_events, many=True, context=self.context).data

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'biography', 'is_owner',
            'signed_up_events', 'owned_events'
        ]