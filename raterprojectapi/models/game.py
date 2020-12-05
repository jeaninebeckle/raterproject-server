from raterprojectapi.views.rating import Ratings
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


    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Ratings.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        # Calculate the averge and return it.
        average = sum(total_rating) / len(total_rating)
