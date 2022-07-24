from django.db import models
from rareapi.models.post import Post
from rareapi.models.rareuser import RareUser

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    created_on = models.DateField()
    