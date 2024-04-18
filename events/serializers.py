from rest_framework import serializers
from events.models import Events
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class EventSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    owner_profile = ProfileSerializer(source='owner.profile', read_only=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user.profile == obj.owner


    class Meta:
        model = Events
        fields = [
            'id', 'is_owner', 'event_name', 'date', 
            'description', 'image', 'owner_profile'
        ]