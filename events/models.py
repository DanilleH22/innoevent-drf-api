from django.db import models
from profiles.models import Profile
from django.contrib.auth.models import User

# Create your models here.

class Events(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(
        upload_to='images/', default='../default_profile_qdjgyp'
        )
    owner = models.ForeignKey(User, related_name='owned_events', on_delete=models.CASCADE)
