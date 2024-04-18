from django.http import Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from innoevent.permissions import IsOwnerOrReadOnly
from events.models import Events
from signup.models import SignUp
from events.serializers import EventSerializer
from signup.serializers import SignUpSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import User


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        profile = self.get_object()
        self.check_object_permissions(request, profile)
        profile_serializer = ProfileSerializer(profile, context={'request': request})

        if request.user.profile.id == int(pk):
            # Events created by the user
            events_created = Events.objects.filter(owner=profile.pk)
            events_created_serializer = EventSerializer(events_created, many=True, context={'request': request})

            # Events the user has signed up for
            signups = SignUp.objects.filter(attendee=profile.pk)
            event_ids = signups.values_list('event', flat=True)
            events_signed_up = Events.objects.filter(id__in=event_ids)
            events_signed_up_serializer = EventSerializer(events_signed_up, many=True, context={'request': request})

            return Response({
                'Profile': profile_serializer.data,
                'Events_created': events_created_serializer.data,
                'Signed_up_for': events_signed_up_serializer.data
            })

        return Response({'Profile': profile_serializer.data})
    
    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)