from django.db import models
from django.contrib.auth.models import User
from rareapi.models.reaction import Reaction

class RareUser(models.Model):
    bio = models.CharField(max_length=150)
    profile_image_url = models.CharField(max_length=1000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reactions = models.ManyToManyField(Reaction, related_name="rareuser")
 