from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Events, SignUp
from .serializers import EventSerializer, SignUpSerializer
from innoevent.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated 
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404


class EventList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = EventSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save(owner=request.user.profile)  
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer = EventSerializer

    def get_object(self, pk):
        try:
            event = Events.objects.get(pk=pk)
            self.check_object_permissions(self.request, event)
            return event
        except Events.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventSignUp(APIView):
    queryset = SignUp.objects.filter()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            sign_up = SignUp.objects.get(pk=pk)
            self.check_object_permissions(self.request, sign_up)
            return sign_up
        except SignUp.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        event = self.get_object(pk=pk)
        # sign_up = SignUp.objects.get(pk=pk)
        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            event = get_object_or_404(Events, id=serializer.validated_data['event'].id)
            attendee = request.user.profile
            if not SignUp.objects.filter(event=event, attendee=attendee).exists():
                SignUp.objects.create(event=event, attendee=attendee)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'User already signed up for this event.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

    