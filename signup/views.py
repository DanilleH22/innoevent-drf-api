from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Events
from signup.models import SignUp
from profiles.models import Profile
from events.serializers import EventSerializer
from .serializers import SignUpSerializer
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters, status


class EventSignUp(APIView):
    """
    USer can sign up to event
    """
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

        if SignUp.objects.filter(event=event, attendee=request.user).exists():
            return Response({"error": "You have already signed up for the event."}, status=status.HTTP_409_CONFLICT)

        data = {
            'event': event.pk, 
            'attendee': request.user.profile,
            'name' : request.data.get('name', ''),
            'email' : request.data.get('email', '')
            }
        serializer = SignUpSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "You have successfully signed up for the event.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
