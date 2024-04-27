from rest_framework.permissions import AllowAny
from .serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import Contact

class ContactUs(CreateAPIView):
    """
    User can fill out a form to contact us 
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

