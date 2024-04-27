from innoevent.permissions import IsOwnerOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve user profile details
    Update profile biography
    Retrieve events created buy the user
    Retrieve events user has signed up to
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)