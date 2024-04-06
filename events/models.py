from django.db import models
from profiles.models import Profile

# Create your models here.

class Events(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(
        upload_to='images/', default='../default_profile_qdjgyp'
        )
    owner = models.ForeignKey(Profile, related_name='owned_events', on_delete=models.CASCADE)


class SignUp(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Profile, related_name='signed_up_events', on_delete=models.CASCADE)