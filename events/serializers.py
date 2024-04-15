from rest_framework import serializers
from events.models import Events, SignUp
from profiles.models import Profile


class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.profile')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')

    
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
    class Meta:
        model = SignUp
        fields = ['event', 'attendee', 'name', 'email']
        read_only_fields = ['attendee']  

    def create(self, validated_data):
        validated_data['attendee'] = self.context['request'].user.profile
        return super().create(validated_data)
