from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    game_image = models.CharField(max_length=100)
    designer = models.CharField(max_length=75, default='') 
