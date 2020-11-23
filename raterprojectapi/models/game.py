from raterprojectapi.models import designer
from django.db import models
from django.db.models.deletion import CASCADE

class Game(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    game_image = models.CharField(max_length=100)
    designer_id = models.ForeignKey("Designer", on_delete=CASCADE, related_name="games", related_query_name="game")
