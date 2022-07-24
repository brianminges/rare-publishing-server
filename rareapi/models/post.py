from django.db import models
from rareapi.models.category import Category
from rareapi.models.rareuser import RareUser
from rareapi.models.reaction import Reaction
from rareapi.models.tag import Tag

class Post(models.Model):
    user = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=1000)
    content = models.CharField(max_length=250)
    approved = models.BigIntegerField()
    tags = models.ManyToManyField(Tag, related_name="tags")
    reactions = models.ManyToManyField(Reaction, related_name="reactions")