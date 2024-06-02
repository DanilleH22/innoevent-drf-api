from rest_framework import serializers
from .models import Profile
from signup.serializers import SignUpSerializer

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    # sign_ups = SignUpSerializer(source='signed_up_events', read_only=True, many=True)
    sign_ups = SignUpSerializer(source='owner.signed_up_events', many=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'biography', 'is_owner',
            'sign_ups'
        ]