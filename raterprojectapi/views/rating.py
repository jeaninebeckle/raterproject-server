"""View module for handling requests about games"""
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

        game = Game.objects.get(pk=request.data["gameId"]) 
        rating.game = game

        rating.player = player

        try:
            rating.save()
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):

        try:
            rating = Rating.objects.get(pk=pk)
            serializer = RatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):

        ratings = Rating.objects.all()

        game = self.request.query_params.get('game', None)
        if game is not None:
            reviews = ratings.filter(game__id=game)

        serializer = RatingSerializer(
            ratings, many=True, context={'request': request})
        return Response(serializer.data)

class RatingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializer type
    """
    class Meta:
        model = Rating
        url = serializers.HyperlinkedIdentityField(
            view_name='review',
            lookup_field='id'
        )
        fields = ('id', 'url', 'value')
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

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
        depth = 1
