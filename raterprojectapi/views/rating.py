"""View module for handling requests about ratings"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Rating, Game, Player

class Ratings(ViewSet):


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized review instance
        """

        player = Player.objects.get(user=request.auth.user)

        rating = Rating()
        rating.value = request.data["value"]

        game = Game.objects.get(pk=request.data["game"]) 
        rating.game = game

        rating.player = player

        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        # for single thing
        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        # for all things
        ratings = Rating.objects.all()

        game = self.request.query_params.get('game', None)
        if game is not None:
            ratings = ratings.filter(game__id=game)
            print(ratings)
            

        serializer = RatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a rating

        Returns:
            Response -- Empty body with 204 status code
        """
        rating = Rating.objects.get(pk=pk)
        rating.value = request.data["value"]
        rating.game = Game.objects.get(pk=request.data["game"]) 
        rating.player = Player.objects.get(user=request.auth.user)

        rating.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializer type
    """
    class Meta:
        model = Rating
        fields = ('id', 'value', 'player', 'game')
        # depth = 1

class RatingUserSerializer(serializers.ModelSerializer):
    """JSON serializer for review player's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class RatingPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for review player"""
    user = RatingUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user']

# class GameSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for games"""
#     class Meta:
#         model = Game
#         fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image', 'average_rating')
#         depth = 1
