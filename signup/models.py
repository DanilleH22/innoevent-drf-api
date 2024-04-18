from django.db import models
from events.models import Events
from django.contrib.auth.models import User

# Create your models here.

class SignUp(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, related_name='signed_up_events', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)