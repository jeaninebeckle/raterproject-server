from django.db import models
from raterprojectapi.models.rating import Rating

class Game(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    est_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    designer = models.CharField(max_length=75, default='')
    categories = models.ManyToManyField("Categories", related_name="categories", related_query_name="category")
 

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        if len(ratings):
            # Sum all of the ratings for the game
            total_rating = 0
            for rating in ratings:
                total_rating += rating.value

            # Calculate the averge and return it.
            average = total_rating / len(ratings)
            return average

        # else: 
        return 0
