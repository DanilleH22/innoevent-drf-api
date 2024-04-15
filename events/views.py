from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Events, SignUp
from profiles.models import Profile
from .serializers import EventSerializer, SignUpSerializer
from innoevent.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import generics
from rest_framework import generics, permissions, filters


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Events.objects.all()

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(owner=profile)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class EventSignUp(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        if not hasattr(request.user, 'profile'):
            return Response({"error": "User profile is required to sign up for events."}, status=status.HTTP_400_BAD_REQUEST)

        data = {'event': event.pk, 'attendee': request.user.profile.pk}
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "You have successfully signed up for the event.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)