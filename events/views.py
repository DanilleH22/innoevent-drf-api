from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Events
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from innoevent.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework import filters


class EventList(generics.ListCreateAPIView):
    """
    List all events
    Filter events so they can be searched
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Events.objects.all().order_by('date')
    filter_backends = [filters.SearchFilter]
    search_fields = ['owner__username', 'event_name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EventCreate(generics.ListCreateAPIView):
    """
    Create an event 
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Events.objects.all().order_by('date')
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get event details
    Update event
    Delete event
    """
    queryset = Events.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj