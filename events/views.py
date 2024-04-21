from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Events
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from innoevent.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Events.objects.all().order_by('date')


class EventCreate(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj