from django.db import models
from django.db.models.deletion import CASCADE

class Review(models.Model):
    description = models.TextField()
    game_id = models.ForeignKey("Game", on_delete=CASCADE, related_name="reviews", related_query_name="review")
    player_id = models.ForeignKey("Player", on_delete=CASCADE, related_name="reviews", related_query_name="review")
