from django.db import models
from django.db.models.deletion import CASCADE

class Rating(models.Model):
    value = models.IntegerField()
    game = models.ForeignKey("Game", on_delete=CASCADE, related_name="ratings", related_query_name="rating")
    player = models.ForeignKey("Player", on_delete=CASCADE, related_name="ratings", related_query_name="rating")

