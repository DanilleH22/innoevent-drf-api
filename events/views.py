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


class EventList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user.profile)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # def get_object(self, pk):
    #     event = get_object_or_404(Events, pk=pk)
    #     self.check_object_permissions(self.request, event)
    #     return event

    # def get(self, request, pk):
    #     event = self.get_object(pk)
    #     serializer = EventSerializer(event, context={'request': request})
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     event = self.get_object(pk)
    #     serializer = EventSerializer(event, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()  
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     event = self.get_object(pk)
    #     event.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class EventSignUp(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        data = {'event': event.pk, 'attendee': request.user.profile.pk} 
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_object(self, pk):
    #     try:
    #         sign_up = SignUp.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, sign_up)
    #         return sign_up
    #     except Profile.DoesNotExist:
    #         raise Http404
    
    # def get(self, request, pk):
    #     sign_up = self.get_object(pk)
    #     # event = get_object_or_404(Events, pk=pk)
    #     serializer = SignUpSerializer(sign_up, context={'request': request})
    #     return Response(serializer.data)

    # def post(self, request, pk):
    #     sign_up = self.get_object(pk)
    #     serializer = SignUpSerializer(sign_up, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Successfully signed up for the event.'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # permission_classes = [IsAuthenticated]

    # def get(self, request, pk):
    #     event = get_object_or_404(Events, pk=pk)
    #     # Ensure the request is passed in the context when initializing the serializer
    #     serializer = EventSerializer(event, context={'request': request})
    #     return Response(serializer.data)

    # def post(self, request, pk):
    #     event = get_object_or_404(Events, pk=pk)
    #     data = request.data.copy()
    #     data['event'] = pk  # Make sure the event ID is correctly included in the request data
    #     serializer = SignUpSerializer(data=data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, pk):
    #     event = get_object_or_404(Events, pk=pk)
    #     data = request.data.copy()
    #     data['event'] = event.pk
    #     serializer = SignUpSerializer(data=data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Successfully signed up for the event.'}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # permission_classes = [IsAuthenticated]

    # def post(self, request, pk):
    #     # Assuming `pk` is the ID of the event to sign up for
    #     event = get_object_or_404(Events, pk=pk)
    #     # Check if the user has already signed up
    #     if SignUp.objects.filter(event=event, attendee=request.user.profile).exists():
    #         return Response({'detail': 'User already signed up for this event.'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     # If not already signed up, create a new sign-up entry
    #     SignUp.objects.create(event=event, attendee=request.user.profile)
    #     return Response({'detail': 'Successfully signed up for the event.'}, status=status.HTTP_201_CREATED)

    # def get(self, request, pk):
    #     # If you want to list all sign-ups for a specific event
    #     sign_ups = SignUp.objects.filter(event__pk=pk)
    #     serializer = SignUpSerializer(sign_ups, many=True)
    #     return Response(serializer.data)
    
    # serializer_class = SignUpSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = SignUp.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['post']

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
    
    # permission_classes = [IsAuthenticated]
    # def get(self, request):
    #     # If you're rendering a blank form for GET requests
    #     serializer = SignUpSerializer(pk=pk)
    #     return Response({'serializer': serializer})

    