from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
import base64
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from raterprojectapi.models import Game, GamePicture, game

class GamePictures(ViewSet):


    def create(self, request):

        game_picture=GamePicture()

        format, imgstr = request.data["game_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["game"]}-{uuid.uuid4()}.{ext}')

        game_picture.action_pic = data
        game = Game.objects.get(pk=request.data["game"])
        game_picture.game = game

        # Give the image property of your game picture instance a value
        # For example, if you named your property `action_pic`, then
        # you would specify the following code:
        #
        #       game_picture.action_pic = data

        # Save the data to the database with the save() method
        try:
            game_picture.save()
            serializer = GamePictureSerializer(game_picture, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class GamePictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamePicture
        fields = ('id', 'game', 'action_pic')


# class GameSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for games"""
#     class Meta:
#         model = Game
#         fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
#         depth = 1
