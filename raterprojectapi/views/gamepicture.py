"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
import base64
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
        """Handle POST operations

        Returns:
            Response -- JSON serialized image instance
        """

        game_picture=GamePicture()

        format, imgstr = request.data["game_image"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["gameId"]}-{uuid.uuid4()}.{ext}')

        game_picture.action_pic = data

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



    def retrieve(self, request, pk=None):

        try:
            game_picture = GamePicture.objects.get(pk=pk)
            serializer = GamePictureSerializer(game_picture, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):

        game_pictures = GamePicture.objects.all()

        game = self.request.query_params.get('game', None)
        if game is not None:
            game_pictures = game_pictures.filter(game__id=game)

        serializer = GamePictureSerializer(
            game_pictures, many=True, context={'request': request})
        return Response(serializer.data)

class GamePictureSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GamePicture
        url = serializers.HyperlinkedIdentityField(
            view_name='gamepicture',
            lookup_field='id'
        )
        fields = ('id', 'url', 'action_pic')


# class GameSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for games"""
#     class Meta:
#         model = Game
#         fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
#         depth = 1
