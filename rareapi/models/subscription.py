from tkinter import CASCADE
from django.db import models
from rareapi.models.rareuser import RareUser

class Subscription(models.Model):
    follower = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="author")
    created_on = models.DateField()
    ended_on = models.DateField(null=True)
    
