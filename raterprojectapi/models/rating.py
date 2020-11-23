from django.db import models
from django.db.models.deletion import CASCADE

class Rating(models.Model):
    value = models.IntegerField()
    player = models.ForeignKey("Player", on_delete=CASCADE)
    game = models.ForeignKey("Game", on_delete=CASCADE)

@property
def average(self):
    return sum(self.value) / len(self.value)
