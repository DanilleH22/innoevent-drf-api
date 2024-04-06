from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Events
from .serializers import EventSerializer
from innoevent.permissions import IsOwnerOrReadOnly


class EventList(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request):
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
