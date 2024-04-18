from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Events
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, permissions
from django.contrib.auth.models import User


class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Events.objects.all().order_by('date')

    def perform_create(self, serializer):
        user = self.request.user  # Get the user instance
        serializer.save(owner=user)



class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj