from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from .game import Game

class GamePicture(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING, related_name="pictures")
    action_pic = models.ImageField(upload_to='actionimages', height_field=None, 
    width_field=None, max_length=None, null=True)
