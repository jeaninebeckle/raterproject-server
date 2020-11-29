"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Player, Designer

class Games(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        player = Player.objects.get(user=request.auth.user)

        game = Game()
        game.title = request.data["title"]
        game.designer_id = request.data["designerId"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.est_time_to_play = request.data["estimatedTimeToPlay"]
        game.age_recommendation = request.data["ageRecommendation"]
        game.game_image = request.data["gameImage"]

        designer = Designer.objects.get(pk=request.data["designerId"]) 
        game.designer = designer

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

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a game

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     gamer = Player.objects.get(user=request.auth.user)

    #     game = Game.objects.get(pk=pk)
    #     game.title = request.data["title"]
    #     game.maker = request.data["maker"]
    #     game.number_of_players = request.data["numberOfPlayers"]
    #     game.skill_level = request.data["skillLevel"]
    #     game.gamer = gamer

    #     category = Category.objects.get(pk=request.data["categoryId"])
    #     game.gametype = gametype
    #     game.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()

        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(gametype__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'description', 'year_released', 'number_of_players', 'est_time_to_play', 'age_recommendation', 'game_image')
        # depth = 1
