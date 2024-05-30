from rest_framework import serializers
from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    created_events = EventSerializer(many=True, read_only=True, source='user.created_events')
    signed_up_events = SignUpSerializer(many=True, read_only=True, source='user.signups')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'biography', 'is_owner', 'created_events',
            'signed_up_events'
        ]