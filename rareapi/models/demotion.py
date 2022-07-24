from django.db import models
from rareapi.models.rareuser import RareUser

class Demotion(models.Model):
    action = models.CharField(max_length=150)
    admin = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="admin")
    approver = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="approver")