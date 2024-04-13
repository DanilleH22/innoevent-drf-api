from rest_framework import serializers
from events.models import Events, SignUp


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='profile')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='profile.id')

    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user.profile == obj.owner


    class Meta:
        model = Events
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'event_name', 'date', 'description', 'image'
        ]


class SignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    email_address = serializers.EmailField()
    
    class Meta:
        model = SignUp
        fields = ['id', 'event', 'name', 'email_address']