from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Events
from .serializers import EventSerializer

class EventList(APIView):
    def get(self, request):
        events = Events.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)