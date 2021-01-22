"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Categories
from django.db.models import Q

class Games(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        game = Game()
        game.title = request.data["title"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.est_time_to_play = request.data["estimatedTimeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.game_image = request.data["gameImage"]
        game.designer = request.data["designer"]
        game.year_released = request.data["yearReleased"]
        categories = Categories.objects.get(pk=request.data["categoryId"])
        game.categories = categories


        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()

        search_text = self.request.query_params.get('q', None)
        if search_text is not None:
            games = games.filter(
                Q(title__contains=search_text) |
                Q(description__contains=search_text) |
                Q(designer__contains=search_text)
            )

        select_text = self.request.query_params.get('orderby', None)
        if select_text is not None:
            games = games.order_by(select_text)

        # add a try and except for field error
        
        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.year_released = request.data["yearReleased"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.est_time_to_play = request.data["estimatedTimeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.designer = request.data["designer"]
        game.categories = request.data["categories"]

        game.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'url', 'label')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        categories = CategorySerializer(many=True)
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'reviews', 'url', 'title', 'description', 'designer', 'year_released', 'categories', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image', 'average_rating')
        depth = 2
