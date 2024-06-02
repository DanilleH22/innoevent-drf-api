from rest_framework import serializers
from events.models import Events
from profiles.models import Profile
# from profiles.serializers import ProfileSerializer


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=["%Y-%m-%d %H:%M:%S", "iso-8601"])

    def get_is_owner(self, obj):
        request = self.context['request']
        return obj.owner == request.user

    class Meta:
        model = Events
        fields = [
            'id', 'event_name', 'date', 
            'description', 'image', 'is_owner',
            'owner'
        ]  