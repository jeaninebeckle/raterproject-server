from django.db import models


class Category(models.Model):
    label = models.CharField(max_length=50)

    # things in quotes should be the model we are linking to
    games = models.ManyToManyField("Game", related_name="categories", related_query_name="category") 
