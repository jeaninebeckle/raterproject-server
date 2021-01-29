"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Review, Game, Player

class Reviews(ViewSet):


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized review instance
        """

        player = Player.objects.get(user=request.auth.user)

        review = Review()
        review.description = request.data["description"]

        game = Game.objects.get(pk=request.data["game"]) 
        review.game = game

        review.player = player

        try:
            review.save()
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):

        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        reviews = Review.objects.all()

        game = self.request.query_params.get('game', None)
        if game is not None:
            reviews = reviews.filter(game__id=game)

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})
        return Response(serializer.data)

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializer type
    """
    class Meta:
        model = Review
        fields = ('id', 'description', 'game', 'player')
        # depth = 1

class ReviewUserSerializer(serializers.ModelSerializer):
    """JSON serializer for review player's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ReviewPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for review player"""
    user = ReviewUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user', 'game_id', 'player_id']

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'url', 'title', 'description', 'designer_id', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
        depth = 1
