from django.shortcuts import render
from rest_framework.permissions import AllowAny
from .serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import Contact
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, permissions

# Create your views here.

# class ContactUs(APIView):
#     def post(self, request):
#         serializer = ContactSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactUs(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

